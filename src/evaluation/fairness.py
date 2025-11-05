"""Fairness evaluation using Fairlearn and Aequitas."""

from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)


def compute_fairness_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    sensitive_features: pd.DataFrame,
    y_proba: Optional[np.ndarray] = None,
) -> Dict[str, Dict[str, float]]:
    """
    Compute fairness metrics across sensitive groups.

    Args:
        y_true: True labels
        y_pred: Predicted labels
        sensitive_features: DataFrame with sensitive attributes
        y_proba: Predicted probabilities (optional)

    Returns:
        Dictionary of fairness metrics per sensitive attribute
    """
    try:
        from fairlearn.metrics import (
            demographic_parity_difference,
            demographic_parity_ratio,
            equalized_odds_difference,
            equalized_odds_ratio,
            MetricFrame,
        )
        from sklearn.metrics import accuracy_score, precision_score, recall_score

    except ImportError:
        logger.error("Fairlearn not installed. Install with: pip install fairlearn")
        return {}

    fairness_results = {}

    for attr in sensitive_features.columns:
        logger.info(f"Computing fairness metrics for: {attr}")

        sensitive_attr = sensitive_features[attr]

        # Demographic parity
        dp_diff = demographic_parity_difference(
            y_true, y_pred, sensitive_features=sensitive_attr
        )
        dp_ratio = demographic_parity_ratio(
            y_true, y_pred, sensitive_features=sensitive_attr
        )

        # Equalized odds
        eo_diff = equalized_odds_difference(
            y_true, y_pred, sensitive_features=sensitive_attr
        )
        eo_ratio = equalized_odds_ratio(
            y_true, y_pred, sensitive_features=sensitive_attr
        )

        # Group metrics
        metric_frame = MetricFrame(
            metrics={
                "accuracy": accuracy_score,
                "precision": precision_score,
                "recall": recall_score,
            },
            y_true=y_true,
            y_pred=y_pred,
            sensitive_features=sensitive_attr,
        )

        fairness_results[attr] = {
            "demographic_parity_difference": dp_diff,
            "demographic_parity_ratio": dp_ratio,
            "equalized_odds_difference": eo_diff,
            "equalized_odds_ratio": eo_ratio,
            "group_metrics": metric_frame.by_group.to_dict(),
            "overall_metrics": metric_frame.overall.to_dict(),
        }

        # Log summary
        logger.info(f"  Demographic Parity Difference: {dp_diff:.4f}")
        logger.info(f"  Equalized Odds Difference: {eo_diff:.4f}")

    return fairness_results


def compute_group_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_proba: Optional[np.ndarray],
    sensitive_features: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute detailed metrics for each sensitive group.

    Args:
        y_true: True labels
        y_pred: Predicted labels
        y_proba: Predicted probabilities
        sensitive_features: DataFrame with sensitive attributes

    Returns:
        DataFrame with metrics per group
    """
    from sklearn.metrics import (
        accuracy_score,
        precision_score,
        recall_score,
        f1_score,
        roc_auc_score,
        confusion_matrix,
    )

    results = []

    for attr in sensitive_features.columns:
        for group in sensitive_features[attr].unique():
            # Filter to group
            mask = sensitive_features[attr] == group

            y_true_group = y_true[mask]
            y_pred_group = y_pred[mask]
            y_proba_group = y_proba[mask] if y_proba is not None else None

            # Compute metrics
            n_samples = len(y_true_group)

            metrics = {
                "attribute": attr,
                "group": group,
                "n_samples": n_samples,
                "base_rate": np.mean(y_true_group),
                "positive_rate": np.mean(y_pred_group),
                "accuracy": accuracy_score(y_true_group, y_pred_group),
                "precision": precision_score(y_true_group, y_pred_group, zero_division=0),
                "recall": recall_score(y_true_group, y_pred_group, zero_division=0),
                "f1": f1_score(y_true_group, y_pred_group, zero_division=0),
            }

            # Add TPR and FPR
            tn, fp, fn, tp = confusion_matrix(y_true_group, y_pred_group).ravel()
            metrics["tpr"] = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            metrics["fpr"] = fp / (fp + tn) if (fp + tn) > 0 else 0.0

            # Add AUROC if probabilities available
            if y_proba_group is not None and len(np.unique(y_true_group)) > 1:
                try:
                    metrics["auroc"] = roc_auc_score(y_true_group, y_proba_group)
                except:
                    metrics["auroc"] = np.nan

            results.append(metrics)

    return pd.DataFrame(results)


def plot_fairness_utility_tradeoff(
    y_true: np.ndarray,
    y_proba: np.ndarray,
    sensitive_features: pd.Series,
    metric: str = "equalized_odds",
    save_path: Optional[str] = None,
) -> plt.Figure:
    """
    Plot fairness-utility tradeoff curve.

    Args:
        y_true: True labels
        y_proba: Predicted probabilities
        sensitive_features: Sensitive attribute (single column)
        metric: Fairness metric to use
        save_path: Optional path to save figure

    Returns:
        Matplotlib figure
    """
    from sklearn.metrics import accuracy_score
    from fairlearn.metrics import equalized_odds_difference

    # Sweep over thresholds
    thresholds = np.linspace(0, 1, 101)
    utilities = []
    fairness_violations = []

    for threshold in thresholds:
        y_pred = (y_proba >= threshold).astype(int)

        # Utility: accuracy
        utility = accuracy_score(y_true, y_pred)
        utilities.append(utility)

        # Fairness: equalized odds difference
        fairness_viol = equalized_odds_difference(
            y_true, y_pred, sensitive_features=sensitive_features
        )
        fairness_violations.append(abs(fairness_viol))

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 6))

    ax.scatter(fairness_violations, utilities, alpha=0.6, s=20)
    ax.plot(fairness_violations, utilities, alpha=0.3, linewidth=1)

    ax.set_xlabel("Fairness Violation (Equalized Odds Difference)", fontsize=12)
    ax.set_ylabel("Utility (Accuracy)", fontsize=12)
    ax.set_title("Fairness-Utility Tradeoff", fontsize=14, fontweight="bold")
    ax.grid(alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        logger.info(f"Saved fairness-utility plot to {save_path}")

    return fig


class FairnessAuditor:
    """Comprehensive fairness auditor using Aequitas."""

    def __init__(self):
        """Initialize fairness auditor."""
        self.audit_results = None

    def audit(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_proba: np.ndarray,
        sensitive_features: pd.DataFrame,
        reference_groups: Optional[Dict[str, str]] = None,
    ) -> pd.DataFrame:
        """
        Conduct comprehensive fairness audit.

        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_proba: Predicted probabilities
            sensitive_features: DataFrame with sensitive attributes
            reference_groups: Dictionary mapping attribute to reference group

        Returns:
            DataFrame with audit results
        """
        try:
            from aequitas.group import Group
            from aequitas.bias import Bias
            from aequitas.fairness import Fairness

        except ImportError:
            logger.error("Aequitas not installed. Install with: pip install aequitas")
            logger.info("Falling back to basic fairness metrics")
            return self._basic_audit(y_true, y_pred, y_proba, sensitive_features)

        # Prepare data for Aequitas
        df = pd.DataFrame(
            {
                "entity_id": range(len(y_true)),
                "score": y_proba,
                "label_value": y_true,
                "pred_label": y_pred,
            }
        )

        # Add sensitive features
        for col in sensitive_features.columns:
            df[col] = sensitive_features[col].values

        # Compute group metrics
        g = Group()
        xtab, _ = g.get_crosstabs(df, attr_cols=list(sensitive_features.columns))

        # Compute bias metrics
        b = Bias()
        bdf = b.get_disparity_predefined_groups(
            xtab,
            original_df=df,
            ref_groups_dict=reference_groups,
            alpha=0.05,
        )

        # Compute fairness determinations
        f = Fairness()
        fdf = f.get_group_value_fairness(bdf)

        self.audit_results = fdf

        logger.info("Fairness audit completed")
        return fdf

    def _basic_audit(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_proba: np.ndarray,
        sensitive_features: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Basic fairness audit without Aequitas.

        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_proba: Predicted probabilities
            sensitive_features: DataFrame with sensitive attributes

        Returns:
            DataFrame with basic audit results
        """
        return compute_group_metrics(y_true, y_pred, y_proba, sensitive_features)

    def generate_report(self, output_path: Optional[str] = None) -> str:
        """
        Generate fairness audit report.

        Args:
            output_path: Optional path to save report

        Returns:
            Report as string
        """
        if self.audit_results is None:
            raise ValueError("No audit results available. Run audit() first.")

        # Generate text report
        report = "=" * 80 + "\n"
        report += "FAIRNESS AUDIT REPORT\n"
        report += "=" * 80 + "\n\n"

        # Summary statistics
        report += "Summary:\n"
        report += f"  Total groups analyzed: {len(self.audit_results)}\n"

        # Detailed results
        report += "\nDetailed Results:\n"
        report += self.audit_results.to_string()

        if output_path:
            with open(output_path, "w") as f:
                f.write(report)
            logger.info(f"Fairness report saved to {output_path}")

        return report
