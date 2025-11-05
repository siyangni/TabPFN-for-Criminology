"""Evaluation modules for metrics, calibration, and fairness."""

from .metrics import compute_classification_metrics, compute_regression_metrics
from .calibration import (
    compute_calibration_metrics,
    plot_reliability_diagram,
    calibrate_predictions,
)
from .fairness import (
    compute_fairness_metrics,
    plot_fairness_utility_tradeoff,
    FairnessAuditor,
)

__all__ = [
    "compute_classification_metrics",
    "compute_regression_metrics",
    "compute_calibration_metrics",
    "plot_reliability_diagram",
    "calibrate_predictions",
    "compute_fairness_metrics",
    "plot_fairness_utility_tradeoff",
    "FairnessAuditor",
]
