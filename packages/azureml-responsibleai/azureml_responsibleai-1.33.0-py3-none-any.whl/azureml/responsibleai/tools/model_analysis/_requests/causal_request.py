# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from typing import List, Optional

from azureml.responsibleai.tools.model_analysis._requests.base_request import BaseRequest


class CausalRequest(BaseRequest):
    def __init__(self,
                 treatment_features: List[str],
                 heterogeneity_features: Optional[List[str]],
                 nuisance_model: str,
                 heterogeneity_model: Optional[str],
                 alpha: Optional[float],
                 upper_bound_on_cat_expansion: int,
                 treatment_cost: float,
                 min_tree_leaf_samples: int,
                 max_tree_depth: int,
                 skip_cat_limit_checks: bool,
                 comment: Optional[str]):
        """Create a request for causal analysis."""
        super(CausalRequest, self).__init__()

        self.treatment_features = treatment_features
        self.heterogeneity_features = heterogeneity_features
        self.nuisance_model = nuisance_model
        self.heterogeneity_model = heterogeneity_model
        self.alpha = alpha
        self.upper_bound_on_cat_expansion = upper_bound_on_cat_expansion
        self.treatment_cost = treatment_cost
        self.min_tree_leaf_samples = min_tree_leaf_samples
        self.max_tree_depth = max_tree_depth
        self.skip_cat_limit_checks = skip_cat_limit_checks
        self.comment = comment
