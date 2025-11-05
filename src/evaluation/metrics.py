"""Core evaluation metrics for classification and regression."""

from typing import Dict, Optional
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    log_loss,
    brier_score_loss,
    mean_squared_error,
    mean_absolute_error,
    r2_score,
    confusion_matrix,
)
import logging

logger = logging.getLogger(__name__)


def compute_classification_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_proba: Optional[np.ndarray] = None,
    average: str = "binary",
) -> Dict[str, float]:
    """
    Compute comprehensive classification metrics.

    Args:
        y_true: True labels
        y_pred: Predicted labels
        y_proba: Predicted probabilities (optional)
        average: Averaging strategy for multi-class

    Returns:
        Dictionary of metrics
    """
    metrics = {}

    # Basic metrics
    metrics["accuracy"] = accuracy_score(y_true, y_pred)
    metrics["precision"] = precision_score(y_true, y_pred, average=average, zero_division=0)
    metrics["recall"] = recall_score(y_true, y_pred, average=average, zero_division=0)
    metrics["f1"] = f1_score(y_true, y_pred, average=average, zero_division=0)

    # Confusion matrix components
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel() if average == "binary" else (0, 0, 0, 0)
    metrics["true_negatives"] = int(tn)
    metrics["false_positives"] = int(fp)
    metrics["false_negatives"] = int(fn)
    metrics["true_positives"] = int(tp)

    # Derived rates
    if tp + fn > 0:
        metrics["tpr"] = tp / (tp + fn)  # True Positive Rate (Recall)
    else:
        metrics["tpr"] = 0.0

    if tn + fp > 0:
        metrics["fpr"] = fp / (tn + fp)  # False Positive Rate
    else:
        metrics["fpr"] = 0.0

    if tn + fn > 0:
        metrics["tnr"] = tn / (tn + fn)  # True Negative Rate (Specificity)
    else:
        metrics["tnr"] = 0.0

    # Probability-based metrics
    if y_proba is not None:
        try:
            # Handle binary vs multi-class
            if y_proba.ndim == 1:
                # Binary probabilities (single column)
                y_proba_binary = y_proba
            elif y_proba.shape[1] == 2:
                # Binary probabilities (two columns)
                y_proba_binary = y_proba[:, 1]
            else:
                # Multi-class
                y_proba_binary = None

            if y_proba_binary is not None:
                metrics["auroc"] = roc_auc_score(y_true, y_proba_binary)
                metrics["auprc"] = average_precision_score(y_true, y_proba_binary)
                metrics["brier"] = brier_score_loss(y_true, y_proba_binary)

            # Log loss works for both binary and multi-class
            metrics["log_loss"] = log_loss(y_true, y_proba)

        except Exception as e:
            logger.warning(f"Error computing probability metrics: {e}")

    return metrics


def compute_regression_metrics(
    y_true: np.ndarray, y_pred: np.ndarray
) -> Dict[str, float]:
    """
    Compute comprehensive regression metrics.

    Args:
        y_true: True values
        y_pred: Predicted values

    Returns:
        Dictionary of metrics
    """
    metrics = {}

    # Core regression metrics
    metrics["mse"] = mean_squared_error(y_true, y_pred)
    metrics["rmse"] = np.sqrt(metrics["mse"])
    metrics["mae"] = mean_absolute_error(y_true, y_pred)
    metrics["r2"] = r2_score(y_true, y_pred)

    # Additional metrics
    residuals = y_true - y_pred
    metrics["mean_residual"] = np.mean(residuals)
    metrics["std_residual"] = np.std(residuals)
    metrics["max_error"] = np.max(np.abs(residuals))

    # Mean Absolute Percentage Error (MAPE)
    # Avoid division by zero
    nonzero_mask = y_true != 0
    if np.any(nonzero_mask):
        mape = np.mean(np.abs((y_true[nonzero_mask] - y_pred[nonzero_mask]) / y_true[nonzero_mask])) * 100
        metrics["mape"] = mape

    return metrics


def bootstrap_ci(
    metric_fn,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_proba: Optional[np.ndarray] = None,
    n_bootstrap: int = 1000,
    confidence: float = 0.95,
    random_state: int = 42,
) -> Dict[str, tuple]:
    """
    Compute bootstrap confidence intervals for metrics.

    Args:
        metric_fn: Function to compute metrics
        y_true: True labels/values
        y_pred: Predicted labels/values
        y_proba: Predicted probabilities (optional)
        n_bootstrap: Number of bootstrap samples
        confidence: Confidence level
        random_state: Random seed

    Returns:
        Dictionary mapping metric names to (lower, upper) CI bounds
    """
    np.random.seed(random_state)

    n_samples = len(y_true)
    metrics_bootstrap = []

    for _ in range(n_bootstrap):
        # Bootstrap sample
        indices = np.random.choice(n_samples, size=n_samples, replace=True)

        y_true_boot = y_true[indices]
        y_pred_boot = y_pred[indices]
        y_proba_boot = y_proba[indices] if y_proba is not None else None

        # Compute metrics
        metrics = metric_fn(y_true_boot, y_pred_boot, y_proba_boot)
        metrics_bootstrap.append(metrics)

    # Compute confidence intervals
    alpha = 1 - confidence
    lower_percentile = (alpha / 2) * 100
    upper_percentile = (1 - alpha / 2) * 100

    cis = {}
    metric_names = metrics_bootstrap[0].keys()

    for metric_name in metric_names:
        values = [m[metric_name] for m in metrics_bootstrap if metric_name in m]
        if values:
            lower = np.percentile(values, lower_percentile)
            upper = np.percentile(values, upper_percentile)
            cis[metric_name] = (lower, upper)

    return cis
