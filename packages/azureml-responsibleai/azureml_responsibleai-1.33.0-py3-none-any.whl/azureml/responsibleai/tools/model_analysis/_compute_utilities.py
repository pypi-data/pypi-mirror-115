# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import argparse
import joblib
import logging
import uuid

from typing import Dict

from azureml._common._error_definition import AzureMLError
from azureml.core import Run
from azureml.exceptions import AzureMLException, UserErrorException

from responsibleai import ModelAnalysis
from responsibleai.serialization_utilities import serialize_json_safe

from azureml.responsibleai.common._errors.error_definitions import (
    MismatchedExperimentName,
    UnexpectedObjectType
)
from azureml.responsibleai.tools.erroranalysis.error_analysis_client import _upload_error_analysis_internal

from azureml.responsibleai.tools.causal.causal_client import _upload_causal_insights_internal
from azureml.responsibleai.tools.counterfactual.counterfactual_examples_client import (
    _upload_counterfactual_examples_internal)
from azureml.responsibleai.tools.model_analysis._model_analysis_explanation_client import (
    ModelAnalysisExplanationClient)

from azureml.responsibleai.tools.model_analysis.model_analysis_run import ModelAnalysisRun
from azureml.responsibleai.tools.model_analysis._compute_dto import ComputeDTO
from azureml.responsibleai.tools.model_analysis._constants import (
    AnalysisTypes,
    AzureMLTypes,
    CausalVersion,
    CounterfactualVersion,
    ErrorAnalysisVersion,
    PropertyKeys)

_logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


def _parse_command_line():
    parser = argparse.ArgumentParser()

    parser.add_argument('--settings_filepath', type=str, required=True,
                        help="Path to the pickled settings")

    return parser.parse_args()


def _run_all_and_upload(settings: ComputeDTO, current_run: Run):
    _logger.info("Found {} explanation requests".format(len(settings.requests.explanation_requests)))
    _logger.info("Found {} causal requests".format(len(settings.requests.causal_requests)))

    _logger.info("Getting the parent run")
    model_analysis_run = ModelAnalysisRun(current_run.experiment, settings.model_analysis_run_id)

    _logger.info("Loading the data")
    train_df = model_analysis_run.get_train_data()
    test_df = model_analysis_run.get_test_data()
    # train_y_pred = model_analysis_run.get_train_labels()
    # test_y_pred = model_analysis_run.get_test_labels()

    _logger.info("Loading the estimator")
    estimator = model_analysis_run.settings.model_loader.load_by_model_id(
        current_run.experiment.workspace,
        model_analysis_run.settings.model_id)

    _logger.info("Creating the local model analysis")
    model_analysis = ModelAnalysis(
        estimator,
        train_df,
        test_df,
        model_analysis_run.settings.target_column_name,
        model_analysis_run.settings.model_type,
        model_analysis_run.settings.categorical_column_names or [],
    )

    _logger.info("Queueing up requests")
    for error_analysis_request in settings.requests.error_analysis_requests:
        model_analysis.error_analysis.add(
            max_depth=error_analysis_request.max_depth,
            num_leaves=error_analysis_request.num_leaves,
            filter_features=error_analysis_request.filter_features,
        )

    for _ in settings.requests.explanation_requests:
        model_analysis.explainer.add()

    for causal_request in settings.requests.causal_requests:
        model_analysis.causal.add(
            treatment_features=causal_request.treatment_features,
            heterogeneity_features=causal_request.heterogeneity_features,
            nuisance_model=causal_request.nuisance_model,
            heterogeneity_model=causal_request.heterogeneity_model,
            alpha=causal_request.alpha,
            upper_bound_on_cat_expansion=causal_request.upper_bound_on_cat_expansion,
            treatment_cost=causal_request.treatment_cost,
            min_tree_leaf_samples=causal_request.min_tree_leaf_samples,
            max_tree_depth=causal_request.max_tree_depth,
            skip_cat_limit_checks=causal_request.skip_cat_limit_checks,
        )

    for request in settings.requests.counterfactual_requests:
        model_analysis.counterfactual.add(method=request.method,
                                          total_CFs=request.total_CFs,
                                          desired_class=request.desired_class,
                                          desired_range=request.desired_range,
                                          permitted_range=request.permitted_range,
                                          features_to_vary=request.features_to_vary,
                                          feature_importance=request.feature_importance)

    _logger.info("Running computations")
    model_analysis.compute()

    _store_explanations(model_analysis, model_analysis_run, settings, current_run)
    _store_error_analysis_reports(model_analysis, model_analysis_run, settings, current_run)
    _store_causal(model_analysis, model_analysis_run, settings, current_run)
    _store_counterfactual(model_analysis, model_analysis_run, settings, current_run)


def _store_error_analysis_reports(rai_analyzer: ModelAnalysis,
                                  parent_ma_run: Run,
                                  settings: ComputeDTO,
                                  current_run: Run):
    _logger.info("Storing error analysis reports")
    all_ea = rai_analyzer.error_analysis.get()
    for i in range(len(all_ea)):
        error_report = all_ea[i]
        comment = settings.requests.error_analysis_requests[i].comment
        datastore_name = parent_ma_run.settings.confidential_datastore_name

        def update_properties(props: Dict[str, str]) -> None:
            props[PropertyKeys.ANALYSIS_TYPE] = AnalysisTypes.ERROR_ANALYSIS_TYPE
            props[PropertyKeys.ANALYSIS_ID] = parent_ma_run.settings.analysis_id
            props[PropertyKeys.VERSION] = str(ErrorAnalysisVersion.V_0)

        ea_asset_id = _upload_error_analysis_internal(current_run,
                                                      error_report,
                                                      AzureMLTypes.MODEL_ANALYSIS,
                                                      update_properties,
                                                      comment=comment,
                                                      datastore_name=datastore_name)
        props = {
            PropertyKeys.ERROR_ANALYSIS_POINTER_FORMAT.format(error_report.id): ea_asset_id
        }
        parent_ma_run.add_properties(props)
    _logger.info("ErrorReports stored")


def _store_counterfactual(model_analysis: ModelAnalysis,
                          model_analysis_run: Run,
                          settings: ComputeDTO,
                          current_run: Run):
    _logger.info("Storing counterfactual")
    cf_examples = model_analysis.counterfactual.get()

    def _update_counterfactual_properties(prop_dict: Dict):
        _logger.info("Modifying properties for counterfactual")
        prop_dict[PropertyKeys.ANALYSIS_TYPE] = AnalysisTypes.COUNTERFACTUAL_TYPE
        prop_dict[PropertyKeys.ANALYSIS_ID] = model_analysis_run.settings.analysis_id
        prop_dict[PropertyKeys.VERSION] = str(CounterfactualVersion.V_0)

    for i, cf_result in enumerate(cf_examples):
        cf_asset_id = _upload_counterfactual_examples_internal(
            current_run,
            counterfactual_examples=cf_result,
            asset_type=AzureMLTypes.MODEL_ANALYSIS,
            update_properties=_update_counterfactual_properties,
            comment=settings.requests.counterfactual_requests[i].comment,
            datastore_name=model_analysis_run.settings.confidential_datastore_name
        )

        props = {
            PropertyKeys.COUNTERFACTUAL_POINTER_FORMAT.format(uuid.uuid4()): cf_asset_id
        }
        model_analysis_run.add_properties(props)
    _logger.info("Counterfactual stored")


def _store_explanations(model_analysis: ModelAnalysis,
                        model_analysis_run: Run,
                        settings: ComputeDTO,
                        current_run: Run):
    _logger.info("Storing explanations")
    client = ModelAnalysisExplanationClient(
        service_context=current_run.experiment.workspace.service_context,
        experiment_name=current_run.experiment,
        run_id=current_run.id,
        _run=current_run,
        datastore_name=model_analysis_run.settings.confidential_datastore_name,
        model_analysis=model_analysis,
        analysis_id=model_analysis_run.settings.analysis_id,
    )

    all_explanations = model_analysis.explainer.get()
    for i in range(len(all_explanations)):
        explanation = all_explanations[i]
        comment = settings.requests.explanation_requests[i].comment
        explanation_asset_id = client._upload_model_explanation_internal(explanation,
                                                                         comment=comment)
        props = {
            PropertyKeys.EXPLANATION_POINTER_FORMAT.format(explanation.id): explanation_asset_id
        }
        model_analysis_run.add_properties(props)
    _logger.info("Explanations stored")


def _store_causal(model_analysis: ModelAnalysis,
                  model_analysis_run: Run,
                  settings: ComputeDTO,
                  current_run: Run):
    _logger.info("Storing causal")

    causal_results = model_analysis.causal.get_data()
    for i, causal_result in enumerate(causal_results):
        serialized_result = serialize_json_safe(causal_result)

        def _update_properties(props):
            _logger.info("Modifying properties for causal")
            props[PropertyKeys.ANALYSIS_TYPE] = AnalysisTypes.CAUSAL_TYPE
            props[PropertyKeys.ANALYSIS_ID] = model_analysis_run.settings.analysis_id
            props[PropertyKeys.VERSION] = str(CausalVersion.V_0)

        asset_id = _upload_causal_insights_internal(
            current_run,
            serialized_result,
            asset_type=AzureMLTypes.MODEL_ANALYSIS,
            update_properties=_update_properties,
            comment=settings.requests.causal_requests[i].comment,
            datastore_name=model_analysis_run.settings.confidential_datastore_name)

        props = {
            PropertyKeys.CAUSAL_POINTER_FORMAT.format(uuid.uuid4()): asset_id
        }
        model_analysis_run.add_properties(props)
    _logger.info("Causal stored")


def _compute_wrapper():
    args = _parse_command_line()

    settings: ComputeDTO = joblib.load(args.settings_filepath)
    if not isinstance(settings, ComputeDTO):
        raise AzureMLException._with_error(
            AzureMLError.create(
                UnexpectedObjectType,
                expected='ComputeDTO',
                actual=str(type(settings))
            )
        )

    my_run = Run.get_context()
    if my_run.experiment.name != settings.experiment_name:
        raise UserErrorException._with_error(
            AzureMLError.create(
                MismatchedExperimentName,
                expected=settings.experiment_name,
                actual=my_run.experiment.name
            )
        )

    _run_all_and_upload(settings, my_run)
