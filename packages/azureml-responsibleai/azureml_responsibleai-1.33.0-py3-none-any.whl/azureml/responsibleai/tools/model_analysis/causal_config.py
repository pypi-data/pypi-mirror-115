# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Configuration for causal analysis runs.

This can be submitted as a child run of a ModelAnalysisRun
"""

from typing import Any, List, Optional

from azureml._base_sdk_common._docstring_wrapper import experimental
from azureml._common._error_definition import AzureMLError
from azureml.core import Workspace, Run
from azureml.core import RunConfiguration
from azureml.core._experiment_method import experiment_method
from azureml.exceptions import UserErrorException

from azureml.responsibleai.tools.model_analysis.model_analysis_run import ModelAnalysisRun

from azureml.responsibleai.tools.model_analysis._requests import CausalRequest
from azureml.responsibleai.common._errors.error_definitions import MismatchedWorkspaceName

from azureml.responsibleai.tools.model_analysis._base_component_config import BaseComponentConfig

from ._requests import RequestDTO


def _submit(config: 'CausalConfig',
            workspace: Workspace,
            experiment_name: str,
            **kwargs: Any) -> Run:
    if workspace.name != config._workspace.name:
        raise UserErrorException._with_error(
            AzureMLError.create(
                MismatchedWorkspaceName,
                expected=config._workspace.name,
                actual=workspace.name
            )
        )
    requests = RequestDTO(causal_requests=config._requests)
    return config.compute_requests(experiment_name, requests, **kwargs)


class _CausalConstants:
    LINEAR_MODEL = 'linear'
    AUTOML_MODEL = 'automl'

    DEFAULT_ALPHA = 0.05
    DEFAULT_UPPER_BOUND_ON_CAT_EXPANSION = 50
    DEFAULT_TREATMENT_COST = 0
    DEFAULT_MIN_TREE_LEAF_SAMPLES = 2
    DEFAULT_MAX_TREE_DEPTH = 3
    DEFAULT_SKIP_CAT_LIMIT_CHECKS = False

    DEFAULT_COMMENT = 'Causal analysis'


@experimental
class CausalConfig(BaseComponentConfig):
    """Configuration for causal analysis runs."""

    @experiment_method(submit_function=_submit)
    def __init__(self,
                 model_analysis_run: ModelAnalysisRun,
                 run_configuration: RunConfiguration = None):
        """Construct a CausalConfig."""
        super(CausalConfig, self).__init__(model_analysis_run, run_configuration)
        self._requests: List[CausalRequest] = []

    def add_request(self,
                    treatment_features: List[str],
                    heterogeneity_features: Optional[List[str]] = None,
                    nuisance_model: str = _CausalConstants.LINEAR_MODEL,
                    heterogeneity_model: Optional[str] = _CausalConstants.LINEAR_MODEL,
                    alpha: Optional[float] = _CausalConstants.DEFAULT_ALPHA,
                    upper_bound_on_cat_expansion: int = _CausalConstants.DEFAULT_UPPER_BOUND_ON_CAT_EXPANSION,
                    treatment_cost: float = _CausalConstants.DEFAULT_TREATMENT_COST,
                    min_tree_leaf_samples: int = _CausalConstants.DEFAULT_MIN_TREE_LEAF_SAMPLES,
                    max_tree_depth: int = _CausalConstants.DEFAULT_MAX_TREE_DEPTH,
                    skip_cat_limit_checks: bool = _CausalConstants.DEFAULT_SKIP_CAT_LIMIT_CHECKS,
                    comment: Optional[str] = _CausalConstants.DEFAULT_COMMENT) -> None:
        """Add a causal insights request to the configuration."""
        request = CausalRequest(treatment_features,
                                heterogeneity_features=heterogeneity_features,
                                nuisance_model=nuisance_model,
                                heterogeneity_model=heterogeneity_model,
                                alpha=alpha,
                                upper_bound_on_cat_expansion=upper_bound_on_cat_expansion,
                                treatment_cost=treatment_cost,
                                min_tree_leaf_samples=min_tree_leaf_samples,
                                max_tree_depth=max_tree_depth,
                                skip_cat_limit_checks=skip_cat_limit_checks,
                                comment=comment)
        self._requests.append(request)
