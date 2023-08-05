# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Dynamic feature suggestions."""

from typing import Any, Dict, List, Optional, Tuple

import logging
import os

import pandas as pd
from azureml.automl.core.featurization import FeaturizationConfig
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared.constants import AutoMLDefaultTimeouts
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.runtime.column_purpose_detection import StatsAndColumnPurposeType
from azureml.automl.runtime.shared.types import DataSingleColumnInputType
from sklearn.pipeline import make_pipeline, Pipeline

logger = logging.getLogger(__name__)


def perform_feature_sweeping(
        task: str,
        X: pd.DataFrame,
        y: DataSingleColumnInputType,
        stats_and_column_purposes: List[StatsAndColumnPurposeType],
        featurization_config: Optional[FeaturizationConfig] = None,
        feature_sweeping_timeout_seconds: int = AutoMLDefaultTimeouts.DEFAULT_FEATSWEEP_TIMEOUT_SECONDS,
        is_cross_validation: bool = True,
        enable_dnn: bool = True,
        force_text_dnn: bool = False,
        feature_sweeping_config: Dict[str, Any] = {},
        working_dir: Optional[str] = None,
        feature_sweeper: Optional[Any] = None) -> List[Tuple[List[str], Pipeline]]:
    """
    Perform feature sweeping and return transforms.

    :param task: Task type.
    :param X: Input data.
    :param y: Input labels.
    :param stats_and_column_purposes: Statistics and column purposes.
    :param featurization_config: Custom featurization configuration if provided by the user.
    :param feature_sweeping_timeout_seconds: Feature sweeping timeout in seconds.
    :param is_cross_validation: If the current scenario is cross validation based.
    :param enable_dnn: If DNN is enabled.
    :param force_text_dnn: If DNN is to be forced.
    :param feature_sweeping_config: Feature sweeping configuration.
    :param working_dir: Working directory.
    :param feature_sweeper: Custom feature sweeper.
    :return: List of transformers to be applied on specific columns.
    """
    transforms = []                     # type: List[Tuple[List[str], Pipeline]]
    Contract.assert_true(feature_sweeping_timeout_seconds > 0,
                         message='feature_sweeping_timeout_seconds must be greater than zero',
                         log_safe=True)
    try:
        logger.info('Feature sweeping timeout: {} seconds.'.format(feature_sweeping_timeout_seconds))
        from azureml.automl.runtime.sweeping.meta_sweeper import MetaSweeper
        feature_sweeper = feature_sweeper or MetaSweeper(
            task=task,
            timeout_sec=feature_sweeping_timeout_seconds,
            is_cross_validation=is_cross_validation,
            featurization_config=featurization_config,
            enable_dnn=enable_dnn,
            force_text_dnn=force_text_dnn,
            feature_sweeping_config=feature_sweeping_config)

        sweeped_transforms = feature_sweeper.sweep(
            working_dir or os.getcwd(),
            X,
            y,
            stats_and_column_purposes)

        if not sweeped_transforms:
            logger.info('Sweeping did not add any transformers.')
        else:
            added_transformers = ','.join(map(get_added_transformer_from_sweeped_transform, sweeped_transforms))
            logger.info('Sweeping added the following transforms: {}'.format(added_transformers))
            for cols, tfs in sweeped_transforms:
                if not isinstance(cols, list):
                    cols = [cols]

                transforms.append((cols, tfs if isinstance(tfs, Pipeline) else make_pipeline(tfs)))
    except Exception as ex:
        logger.info("Sweeping failed with an error.")
        logging_utilities.log_traceback(exception=ex, logger=logger, is_critical=False)

    return transforms


def get_added_transformer_from_sweeped_transform(sweeped_transform: Tuple[str, Pipeline]) -> str:
    """
    Get the name of a transformer added during feature sweeping.

    :param sweeped_transform: A tuple containing the pipeline with the transformer in it generated by the MetaSweeper.
    :return: The name of the transformer object.
    """
    pipeline = sweeped_transform[1]
    return _pipeline_name_(pipeline)


def _pipeline_name_(pipeline: Pipeline) -> str:
    """
    Method for extracting the name of the last transformer in a pipeline.

    :param pipeline: The input pipeline.
    :return: The name of the last transformer or 'Unknown' if pipeline is None.
    """
    if pipeline is not None:
        if isinstance(pipeline, Pipeline):
            return type(pipeline.steps[-1][1]).__name__
        return type(pipeline).__name__

    return "Unknown"
