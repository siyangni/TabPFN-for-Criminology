"""Calibration evaluation and post-hoc calibration methods."""

from typing import Dict, Optional, Tuple
import numpy as np
import matplotlib.pyplot as plt
from sklearn.calibration import calibration_curve, CalibratedClassifierCV
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import brier_score_loss, log_loss
import logging

logger = logging.getLogger(__name__)


def compute_calibration_metrics(
    y_true: np.ndarray,
    y_proba: np.ndarray,
    n_bins: int = 10,
) -> Dict[str, float]:
    """
    Compute calibration metrics.

    Args:
        y_true: True binary labels
        y_proba: Predicted probabilities for positive class
        n_bins: Number of bins for ECE

    Returns:
        Dictionary of calibration metrics
    """
    metrics = {}

    # Brier score
    metrics["brier_score"] = brier_score_loss(y_true, y_proba)

    # Log loss
    # Convert to 2D array for log_loss
    y_proba_2d = np.column_stack([1 - y_proba, y_proba])
    metrics["log_loss"] = log_loss(y_true, y_proba_2d)

    # Expected Calibration Error (ECE)
    ece = compute_ece(y_true, y_proba, n_bins=n_bins)
    metrics["ece"] = ece

    # Maximum Calibration Error (MCE)
    mce = compute_mce(y_true, y_proba, n_bins=n_bins)
    metrics["mce"] = mce

    return metrics


def compute_ece(
    y_true: np.ndarray, y_proba: np.ndarray, n_bins: int = 10
) -> float:
    """
    Compute Expected Calibration Error.

    ECE = sum over bins of |accuracy - confidence| * proportion of samples in bin

    Args:
        y_true: True labels
        y_proba: Predicted probabilities
        n_bins: Number of bins

    Returns:
        ECE value
    """
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    bin_lowers = bin_boundaries[:-1]
    bin_uppers = bin_boundaries[1:]

    ece = 0.0
    for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
        # Find samples in this bin
        in_bin = (y_proba > bin_lower) & (y_proba <= bin_upper)
        prop_in_bin = np.mean(in_bin)

        if prop_in_bin > 0:
            # Average confidence in bin
            avg_confidence = np.mean(y_proba[in_bin])
            # Average accuracy in bin
            avg_accuracy = np.mean(y_true[in_bin])
            # Add to ECE
            ece += np.abs(avg_accuracy - avg_confidence) * prop_in_bin

    return ece


def compute_mce(
    y_true: np.ndarray, y_proba: np.ndarray, n_bins: int = 10
) -> float:
    """
    Compute Maximum Calibration Error.

    MCE = max over bins of |accuracy - confidence|

    Args:
        y_true: True labels
        y_proba: Predicted probabilities
        n_bins: Number of bins

    Returns:
        MCE value
    """
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    bin_lowers = bin_boundaries[:-1]
    bin_uppers = bin_boundaries[1:]

    mce = 0.0
    for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
        in_bin = (y_proba > bin_lower) & (y_proba <= bin_upper)

        if np.sum(in_bin) > 0:
            avg_confidence = np.mean(y_proba[in_bin])
            avg_accuracy = np.mean(y_true[in_bin])
            calibration_error = np.abs(avg_accuracy - avg_confidence)
            mce = max(mce, calibration_error)

    return mce


def plot_reliability_diagram(
    y_true: np.ndarray,
    y_proba: np.ndarray,
    n_bins: int = 10,
    title: str = "Reliability Diagram",
    save_path: Optional[str] = None,
) -> plt.Figure:
    """
    Plot reliability (calibration) diagram.

    Args:
        y_true: True labels
        y_proba: Predicted probabilities
        n_bins: Number of bins
        title: Plot title
        save_path: Optional path to save figure

    Returns:
        Matplotlib figure
    """
    # Compute calibration curve
    prob_true, prob_pred = calibration_curve(y_true, y_proba, n_bins=n_bins, strategy="uniform")

    # Compute metrics
    ece = compute_ece(y_true, y_proba, n_bins=n_bins)
    brier = brier_score_loss(y_true, y_proba)

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8))

    # Plot perfect calibration line
    ax.plot([0, 1], [0, 1], "k--", label="Perfect Calibration", linewidth=2)

    # Plot calibration curve
    ax.plot(
        prob_pred,
        prob_true,
        marker="o",
        linewidth=2,
        label=f"Model (ECE={ece:.3f}, Brier={brier:.3f})",
    )

    # Formatting
    ax.set_xlabel("Mean Predicted Probability", fontsize=12)
    ax.set_ylabel("Fraction of Positives", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.legend(loc="upper left", fontsize=10)
    ax.grid(alpha=0.3)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        logger.info(f"Saved reliability diagram to {save_path}")

    return fig


class TemperatureScaling:
    """Temperature scaling for probability calibration."""

    def __init__(self):
        """Initialize temperature scaling."""
        self.temperature = 1.0

    def fit(self, y_proba_logits: np.ndarray, y_true: np.ndarray) -> "TemperatureScaling":
        """
        Fit temperature parameter.

        Args:
            y_proba_logits: Logits (before softmax)
            y_true: True labels

        Returns:
            Fitted calibrator
        """
        from scipy.optimize import minimize

        def nll(temp):
            # Apply temperature scaling
            scaled_logits = y_proba_logits / temp
            # Compute softmax
            scaled_proba = self._softmax(scaled_logits)
            # Compute negative log-likelihood
            return log_loss(y_true, scaled_proba)

        # Optimize temperature
        result = minimize(nll, x0=1.0, method="Nelder-Mead")
        self.temperature = result.x[0]

        logger.info(f"Fitted temperature: {self.temperature:.4f}")
        return self

    def transform(self, y_proba_logits: np.ndarray) -> np.ndarray:
        """
        Apply temperature scaling.

        Args:
            y_proba_logits: Logits to scale

        Returns:
            Calibrated probabilities
        """
        scaled_logits = y_proba_logits / self.temperature
        return self._softmax(scaled_logits)

    @staticmethod
    def _softmax(logits: np.ndarray) -> np.ndarray:
        """Compute softmax."""
        exp_logits = np.exp(logits - np.max(logits, axis=-1, keepdims=True))
        return exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)


def calibrate_predictions(
    y_proba: np.ndarray,
    y_true: np.ndarray,
    method: str = "isotonic",
) -> np.ndarray:
    """
    Calibrate probabilities using post-hoc methods.

    Args:
        y_proba: Predicted probabilities (n_samples,) for binary
        y_true: True labels
        method: Calibration method ("isotonic" or "platt")

    Returns:
        Calibrated probabilities
    """
    if method == "isotonic":
        calibrator = IsotonicRegression(out_of_bounds="clip")
        calibrated_proba = calibrator.fit_transform(y_proba, y_true)

    elif method == "platt":
        # Platt scaling = logistic regression on probabilities
        from sklearn.linear_model import LogisticRegression

        calibrator = LogisticRegression()
        calibrator.fit(y_proba.reshape(-1, 1), y_true)
        calibrated_proba = calibrator.predict_proba(y_proba.reshape(-1, 1))[:, 1]

    else:
        raise ValueError(f"Unknown calibration method: {method}")

    logger.info(
        f"Calibrated using {method}. "
        f"Before ECE: {compute_ece(y_true, y_proba):.4f}, "
        f"After ECE: {compute_ece(y_true, calibrated_proba):.4f}"
    )

    return calibrated_proba
