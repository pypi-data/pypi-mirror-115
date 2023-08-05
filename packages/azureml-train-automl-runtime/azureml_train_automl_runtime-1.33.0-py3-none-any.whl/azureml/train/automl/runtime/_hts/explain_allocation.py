# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, Dict, List, Optional, cast

import json
import logging
import os

import pandas as pd

import azureml.train.automl.runtime._hts.hts_runtime_utilities as hru

from joblib import Parallel, delayed

from azureml.core import Run
from azureml.train.automl.constants import HTSConstants
from azureml.train.automl.runtime._hts import allocation_utilities
from azureml.train.automl.runtime._hts.hts_graph import Graph
from azureml.automl.core._logging.event_logger import EventLogger
import azureml.train.automl.runtime._hts.hts_events as hts_events
from azureml.train.automl.runtime._hts.hts_node import Node
from azureml.automl.core.shared._diagnostics.automl_error_definitions import ExplanationsNotFound
from azureml.automl.core.shared.exceptions import ClientException
from azureml._common._error_definition.azureml_error import AzureMLError
from azureml.automl.core.shared.reference_codes import ReferenceCodes


logger = logging.getLogger(__name__)


def explain_allocation_driver(arguments_dict: Dict[str, Any],
                              script_run: Run,
                              event_logger: EventLogger) -> None:
    """
    Explanation allocation driver for python script steps.

    This method should be called from a python script step, used in conjunction with explain_parallel_driver.
    This method will take explanations at the training level produced by calling explain_parallel_driver
    and allocate them.
    * Models on training level will have explanations directly (best model explanation is enabled by default)
    * Models above training level will get explanations using proportional/weighted
      aggregations from explanations for training level models
    *

    Rather than returning the allocated predictions, this method writes them to the output directory,
    as specified in the arguments_dict.

    :param arguments_dict: The arguments used for this script.
    :param script_run: The script run.
    :param event_logger: The event logger.
    :returns: None.
    """
    custom_dim = hru.get_additional_logging_custom_dim(HTSConstants.STEP_EXPLAIN_ALLOCATION)
    hru.update_log_custom_dimension(custom_dim)
    event_logger_additional_fields = hru.get_event_logger_additional_fields(custom_dim, script_run.parent.id)
    event_logger.log_event(hts_events.HTSExplAllocationStart(event_logger_additional_fields))

    explain_level = arguments_dict.get(HTSConstants.FORECAST_LEVEL)
    input = arguments_dict[HTSConstants.EXPLANATION_DIR]
    enable_engineered_explanations = hru.str_or_bool_to_boolean(
        arguments_dict[HTSConstants.ENGINEERED_EXPLANATION])
    output = arguments_dict[HTSConstants.OUTPUT_PATH]
    graph = Graph.get_graph_from_file(arguments_dict[HTSConstants.HTS_GRAPH])

    event_logger.log_event(hts_events.HTSExplAllocationAllocation(event_logger_additional_fields))

    all_levels = graph.hierarchy + [HTSConstants.HTS_ROOT_NODE_LEVEL]
    desired_levels = all_levels if explain_level is None else [explain_level]
    _explain(graph, desired_levels, input, output, True, event_logger, event_logger_additional_fields)
    if enable_engineered_explanations:
        _explain(graph, desired_levels, input, output, False, event_logger, event_logger_additional_fields)

    event_logger.log_event(hts_events.HTSExplAllocationEnd(event_logger_additional_fields))


def _explain(graph: Graph,
             desired_levels: List[str],
             input_path: str,
             output_path: str,
             is_raw: bool,
             event_logger: EventLogger,
             custom_dim: Dict[str, str]) -> None:
    """
    Aggregate and allocate the explanations on all levels.

    :param graph: The hierarchy graph.
    :param desired_levels: The levels for which the explanations are requested.
    :param input_path: The dirrectory with explanations generated by the training run.
    :param output_path: The directory to write the files to.
    :param is_raw: The file with raw or engineered featues explanations.
    :param event_logger: The event logger.
    :param custom_dim: Additional properties for logging.
    """
    event_logger.log_event(hts_events.HTSExplAllocationRawData(custom_dim))
    explain_df = read_all_explanations(input_path, graph, is_raw, False)

    expl_type = (HTSConstants.EXPLANATIONS_RAW_FEATURES if is_raw else
                 HTSConstants.EXPLANATIONS_ENGINEERED_FEATURES)
    if(len(explain_df) == 0):
        logger.info("No explanations for {} features found.".format(
            expl_type))
        return

    logger.info("Successfully retrieved {} explanations.".format(expl_type))
    os.makedirs(output_path, exist_ok=True)

    # Run explanations in parallel if possible.
    cpu_cnt = os.cpu_count()
    if cpu_cnt is None or cpu_cnt <= 1:
        # There is only one core, or we did non detected cores.
        for lvl in desired_levels:
            _explain_one_level(explain_df, graph, output_path, lvl, is_raw)
    else:
        # Several cores were detected, run in parallel.
        Parallel(n_jobs=cpu_cnt)(delayed(_explain_one_level)(
            explain_df, graph,
            output_path, lvl, is_raw) for lvl in desired_levels)


def _explain_one_level(
        explain_df: pd.DataFrame,
        graph: Graph,
        out_dir: str,
        explain_level: str,
        is_raw: bool
) -> None:
    """
    Aggregate or allocate the explanation on one level.

    :param explain_df: The data frame with explanations from the training level.
    :param graph: The hierarchy graph.
    :param out_dir: The dirrectory to write the files to.
    :param explain_level: The level of explanations.
    :param is_raw: The file with raw or engineered featues explanations.
    """
    # If explanation level is not in the hierarchy_to_training_level, it is below it and
    # disaggregation is needed. The edge case is HTS_ROOT_NODE_LEVEL, which is never in
    # the hierarchy and in this case disaggregation is not needed.
    disaggregation_needed = (
        explain_level not in graph.hierarchy_to_training_level and
        explain_level != HTSConstants.HTS_ROOT_NODE_LEVEL
    )

    if disaggregation_needed:
        logger.info("Explanation level below training level, disaggregating to leaf nodes.")
        res = allocation_utilities.disaggregate_predictions(
            explain_df,
            graph,
            "",
            {},
            disaggregate_one_node,
            explain_level)
    else:
        logger.info("Explanation level above training level, no disaggregation required.")

        # If the explanation level is equal to the training level, or the forecast level is the leaf node level,
        # no aggregation is required.
        aggregation_needed = explain_level != graph.training_level and (
            explain_level == HTSConstants.HTS_ROOT_NODE_LEVEL or explain_level in graph.hierarchy_to_training_level)

        if aggregation_needed:
            logger.info("Explanation level is above training level, beginning aggregation.")
            # If we are explaining above the training level, we are estimating the averages of all
            # explanations, included in the groups.
            if explain_level == HTSConstants.HTS_ROOT_NODE_LEVEL:
                # The root level is special, because it includes all groups.
                means_series = explain_df.apply('mean', axis=0)
                res = pd.DataFrame([means_series.values], columns=means_series.index)
            else:
                # Calculate averages only by groups which have to be merged.
                group_columns = graph.hierarchy[:graph.hierarchy.index(explain_level) + 1]
                res = explain_df.groupby(group_columns, as_index=False, group_keys=False).mean()
        else:
            logger.info("Explanation level is at training level.")
            res = explain_df

    res.to_csv(
        _get_file_name(out_dir, explain_level, is_raw),
        index=False)


def _get_file_name(out_dir: str, explain_level: str, is_raw: bool, separator: str = '_') -> str:
    """
    Generate the name for the explanations file.

    :param out_dir: The dirrectory to write the files to.
    :param explain_level: The level of explanations.
    :param is_raw: The file with raw or engineered featues explanations.
    :param separator: The separator to be used in the file name.
    :return: The string with the path to be used to save the file.
    """
    if is_raw:
        file_name_lst = [HTSConstants.EXPLANATIONS_RAW_FEATURES]
    else:
        file_name_lst = [HTSConstants.EXPLANATIONS_ENGINEERED_FEATURES]
    file_name_lst.append('explanations')
    file_name_lst.append(explain_level + '.csv')
    return os.path.join(out_dir, separator.join(file_name_lst))


def read_all_explanations(explanation_dir: str, graph: Graph, raw: bool,
                          except_on_no_explanation: bool) -> pd.DataFrame:
    """
    Read all the explanations and organize it to the data frame.

    :param explanation_dir: The directory with the explanations.
    :param graph: The hierarchy graph.
    :param raw: If True, raw explanations will be used, engineered
                explanations will be used otherwise.
    :param except_on_no_explanation: Raise an exception if the explanation is absent.
    :return: The data frame with collected explanations.
    """
    node_list = graph.get_children_of_level(cast(Node, graph.root), graph.training_level)
    explanation_dir = os.path.join(explanation_dir, HTSConstants.HTS_DIR_EXPLANATIONS)
    expanation_list = []
    if os.path.isdir(explanation_dir):
        file_list = os.listdir(explanation_dir)
        for node in node_list:
            file_name = hru.get_explanation_artifact_name(raw, node.node_id)
            if file_name not in file_list:
                logger.warn("The file {} was not found. The explanations may not be coherent.".format(file_name))
                continue
            with open(os.path.join(explanation_dir, file_name)) as f:
                artifacts_dict = json.load(f)
            current_node = node
            while current_node.name != HTSConstants.HTS_ROOT_NODE_NAME:
                artifacts_dict[current_node.level] = current_node.name
                current_node = cast(Node, current_node.parent)
            expanation_list.append(artifacts_dict)
    if not expanation_list:
        if except_on_no_explanation:
            expl_type = (HTSConstants.EXPLANATIONS_RAW_FEATURES if raw else
                         HTSConstants.EXPLANATIONS_ENGINEERED_FEATURES)
            raise ClientException._with_error(
                AzureMLError.create(ExplanationsNotFound,
                                    exp_type=expl_type,
                                    target='explanations',
                                    reference_code=ReferenceCodes._HTS_NO_EXPLANATION)
            )
        else:
            return pd.DataFrame()
    return pd.DataFrame(expanation_list)


def disaggregate_one_node(df: pd.DataFrame,
                          node: Node,
                          graph: Graph,
                          parsed_metadata: Dict[str, Any],
                          allocation_method: str,
                          target_level: Optional[str]
                          ) -> pd.DataFrame:
    """
    Add bottom level nodes to the dataframe.

    This method takes a node and dataframe, and creates duplicate copies of the dataframe with the entire
    hierarchy from node to leaf nodes included.
    :param node: The node to be used as a template.
    :param grapg: The hierarchy graph generated during training.
    :param parsed_metadata: The metadata. Not used, added for function signature.
    :param allocation_method: The mehod used for allocation. Not used, added for function signature.
    :param target_level: The target explanation level.
    :return:  duplicate copies of the dataframe with the entire hierarchy.
    """
    if target_level is None:
        # This is mypy fix as we always provide target_level to this function.
        return pd.DataFrame()
    # If training index is root, well add the entire hierarchy
    # otherwise we only need to update the nodes from training to leaf.
    if graph.training_level != HTSConstants.HTS_ROOT_NODE_LEVEL:
        start_col = graph.hierarchy.index(graph.training_level) + 1
    else:
        start_col = 0
    end_col = graph.hierarchy.index(target_level)
    explanation_cols = list(filter(lambda col: col not in graph.hierarchy, df.columns))

    logger.info("retrieving children for node: {}".format(node.node_id))
    children = graph.get_children_of_level(node, target_level)

    if children:
        results = []
        for child in children:
            # Update all our predictions so all leaf nodes are represented.
            c_pred = df.copy(deep=True)
            runner = child
            for i in range(start_col, end_col + 1):
                # Update the hierarchy with of each leaf node with
                # the child's relative tree path up to training level.
                c_pred[runner.level] = runner.name
                # order the data frame to look better.
                runner = cast(Node, runner.parent)
            c_pred = c_pred[graph.hierarchy[:end_col + 1] + explanation_cols]
            results.append(c_pred)
        logger.info("Updated explanations for {} children.".format(len(children)))
        return pd.concat(results, sort=False, ignore_index=True)
    # If there is no children, just return the initial data frame.
    return df.copy(deep=True)
