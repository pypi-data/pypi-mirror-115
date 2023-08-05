# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Configuration for counterfactual analysis runs.

This can be submitted as a child run of a ModelAnalysisRun
"""
from responsibleai._managers.counterfactual_manager import CounterfactualConstants
from typing import Any, List, Optional, Union, Dict

from azureml._base_sdk_common._docstring_wrapper import experimental
from azureml._common._error_definition import AzureMLError
from azureml.core import Workspace, Run
from azureml.core import RunConfiguration
from azureml.core._experiment_method import experiment_method
from azureml.exceptions import UserErrorException

from azureml.responsibleai.tools.model_analysis.model_analysis_run import ModelAnalysisRun

from azureml.responsibleai.tools.model_analysis._requests import CounterfactualRequest
from azureml.responsibleai.common._errors.error_definitions import MismatchedWorkspaceName

from azureml.responsibleai.tools.model_analysis._base_component_config import BaseComponentConfig

from ._requests import RequestDTO


def cf_submit(config: 'CounterfactualConfig',
              workspace: Workspace,
              experiment_name: str,
              **kwargs: Any) -> Run:
    """
    Submit a run to add counterfactuals.

    :param config:
    :param workspace:
    :param experiment_name:
    :param kwargs:
    :return:
    """
    if workspace.name != config._workspace.name:
        raise UserErrorException._with_error(
            AzureMLError.create(
                MismatchedWorkspaceName,
                expected=config._workspace.name,
                actual=workspace.name
            )
        )
    requests = RequestDTO(counterfactual_requests=config._requests)
    return config.compute_requests(experiment_name, requests, **kwargs)


@experimental
class CounterfactualConfig(BaseComponentConfig):
    """Configuration for counterfactual analysis runs."""

    @experiment_method(submit_function=cf_submit)
    def __init__(self,
                 model_analysis_run: ModelAnalysisRun,
                 run_configuration: RunConfiguration = None):
        """Construct a CounterfactualConfig."""
        super(CounterfactualConfig, self).__init__(model_analysis_run, run_configuration)
        self._requests: List[CounterfactualRequest] = []

    def add_request(self,
                    total_CFs: int,
                    method: str = CounterfactualConstants.RANDOM,
                    desired_class: Union[str, int] = CounterfactualConstants.OPPOSITE,
                    desired_range: Optional[List[float]] = None,
                    feature_importance: bool = True,
                    features_to_vary: Union[List[str], str] = 'all',
                    permitted_range: Optional[Dict[str, List[float]]] = None,
                    comment: Optional[str] = "counterfactual_request"):
        """Add a counterfactual request to the configuration.

        :param total_CFs: Total number of counterfactuals required.
        :type total_CFs: int
        :param method: Type of dice-ml explainer. Either of "random", "genetic" or "kdtree".
        :type method: str
        :param desired_class: Desired counterfactual class. For binary
                              classification, this needs to be set as
                              "opposite".
        :type desired_class: string or int
        :param desired_range: For regression problems.
                              Contains the outcome range
                              to generate counterfactuals in.
        :type desired_range: list[float]
        :param permitted_range: Dictionary with feature names as keys and
                                permitted range in list as values.
                                Defaults to the range inferred from training
                                data.
        :type permitted_range: dict
        :param features_to_vary: Either a string "all" or a list of
                                 feature names to vary.
        :type features_to_vary: list
        :param feature_importance: Flag to compute feature importance using
                                   dice-ml.
        :type feature_importance: bool
        :param comment: Comment to identify the counterfactual.
        :type comment: str
        """
        request = CounterfactualRequest(total_CFs=total_CFs,
                                        method=method,
                                        desired_class=desired_class,
                                        desired_range=desired_range,
                                        feature_importance=feature_importance,
                                        permitted_range=permitted_range,
                                        features_to_vary=features_to_vary,
                                        comment=comment)
        self._requests.append(request)
