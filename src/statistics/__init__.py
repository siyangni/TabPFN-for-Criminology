"""Statistical inference utilities for TabPFN criminology research.

This module provides statistical testing, effect size calculation, and
inference functions tailored for criminal justice prediction research.

Modules:
    hypothesis_tests: Statistical tests for model comparison
    effect_sizes: Effect size calculations and interpretations
    power_analysis: Power and sample size calculations
    multiple_comparisons: Correction methods for multiple testing
    diagnostics: Model diagnostic statistics
"""

from .hypothesis_tests import (
    mcnemar_test,
    delong_test,
    permutation_test,
    bootstrap_test,
)

from .effect_sizes import (
    cohens_d,
    cohens_h,
    cramers_v,
    risk_difference,
    risk_ratio,
    odds_ratio,
    number_needed_to_evaluate,
)

from .multiple_comparisons import (
    bonferroni_correction,
    holm_correction,
    benjamini_hochberg,
    false_discovery_rate,
)

__all__ = [
    # Hypothesis tests
    "mcnemar_test",
    "delong_test",
    "permutation_test",
    "bootstrap_test",
    # Effect sizes
    "cohens_d",
    "cohens_h",
    "cramers_v",
    "risk_difference",
    "risk_ratio",
    "odds_ratio",
    "number_needed_to_evaluate",
    # Multiple comparisons
    "bonferroni_correction",
    "holm_correction",
    "benjamini_hochberg",
    "false_discovery_rate",
]
