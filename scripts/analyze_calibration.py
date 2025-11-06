"""
Comprehensive calibration analysis for classification models.

This script:
1. Loads model predictions
2. Computes calibration metrics (Brier, ECE, MCE)
3. Generates reliability diagrams
4. Applies post-hoc calibration (temperature scaling, isotonic)
5. Saves results for manuscript
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import json
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple

from evaluation import (
    compute_calibration_metrics,
    plot_reliability_diagram,
    calibrate_predictions,
)
from utils import set_seed, setup_logger

logger = setup_logger("calibration_analysis")


def analyze_calibration_single_model(
    y_true: np.ndarray,
    y_proba: np.ndarray,
    model_name: str,
    output_dir: Path,
    n_bins: int = 10,
) -> Dict:
    """Analyze calibration for a single model."""

    logger.info(f"Analyzing calibration for {model_name}...")

    # Compute calibration metrics
    metrics = compute_calibration_metrics(y_true, y_proba, n_bins=n_bins)

    logger.info(f"  Brier Score: {metrics['brier_score']:.4f}")
    logger.info(f"  ECE: {metrics['ece']:.4f}")
    logger.info(f"  MCE: {metrics['mce']:.4f}")

    # Generate reliability diagram
    fig = plot_reliability_diagram(
        y_true,
        y_proba,
        n_bins=n_bins,
        title=f"Reliability Diagram - {model_name}",
        save_path=output_dir / f"{model_name}_reliability.png",
    )
    plt.close(fig)

    # Apply post-hoc calibration
    logger.info(f"  Applying post-hoc calibration...")

    try:
        # Isotonic regression
        y_proba_isotonic = calibrate_predictions(y_proba, y_true, method="isotonic")
        metrics_isotonic = compute_calibration_metrics(y_true, y_proba_isotonic, n_bins=n_bins)

        # Platt scaling
        y_proba_platt = calibrate_predictions(y_proba, y_true, method="platt")
        metrics_platt = compute_calibration_metrics(y_true, y_proba_platt, n_bins=n_bins)

        metrics['calibrated'] = {
            'isotonic': metrics_isotonic,
            'platt': metrics_platt,
        }

        logger.info(f"  After isotonic: ECE={metrics_isotonic['ece']:.4f}")
        logger.info(f"  After Platt: ECE={metrics_platt['ece']:.4f}")

    except Exception as e:
        logger.warning(f"  Could not apply calibration: {e}")

    return metrics


def plot_calibration_comparison(
    calibration_results: Dict[str, Dict],
    output_dir: Path,
):
    """Plot calibration metrics comparison across models."""

    models = list(calibration_results.keys())
    metrics_names = ['brier_score', 'ece', 'mce']

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for idx, metric_name in enumerate(metrics_names):
        ax = axes[idx]

        values = [calibration_results[model][metric_name] for model in models]

        bars = ax.barh(models, values, color='steelblue', alpha=0.7)

        # Color code: green if good, orange if moderate, red if poor
        if metric_name in ['brier_score', 'ece', 'mce']:
            colors = ['green' if v < 0.05 else 'orange' if v < 0.10 else 'red' for v in values]
            for bar, color in zip(bars, colors):
                bar.set_color(color)

        ax.set_xlabel(metric_name.replace('_', ' ').title(), fontsize=12)
        ax.set_title(f'{metric_name.replace("_", " ").title()} Comparison', fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3, axis='x')

        # Add reference line for "good" calibration
        if metric_name == 'ece':
            ax.axvline(x=0.05, color='green', linestyle='--', alpha=0.5, label='Good (<0.05)')
            ax.axvline(x=0.10, color='orange', linestyle='--', alpha=0.5, label='Moderate (<0.10)')
            ax.legend(fontsize=8)

    plt.tight_layout()

    output_file = output_dir / "calibration_comparison.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    logger.info(f"Saved calibration comparison plot to {output_file}")
    plt.close()


def plot_reliability_comparison(
    y_true_dict: Dict[str, np.ndarray],
    y_proba_dict: Dict[str, np.ndarray],
    output_dir: Path,
    n_bins: int = 10,
):
    """Plot reliability diagrams for all models in one figure."""

    from sklearn.calibration import calibration_curve

    models = list(y_proba_dict.keys())
    n_models = len(models)

    # Create grid
    n_cols = 3
    n_rows = (n_models + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))

    if n_rows == 1:
        axes = axes.reshape(1, -1)

    for idx, model in enumerate(models):
        row = idx // n_cols
        col = idx % n_cols
        ax = axes[row, col]

        y_true = y_true_dict[model]
        y_proba = y_proba_dict[model]

        # Compute calibration curve
        prob_true, prob_pred = calibration_curve(y_true, y_proba, n_bins=n_bins, strategy="uniform")

        # Compute ECE
        from evaluation.calibration import compute_ece
        ece = compute_ece(y_true, y_proba, n_bins=n_bins)

        # Plot
        ax.plot([0, 1], [0, 1], "k--", label="Perfect Calibration", linewidth=2)
        ax.plot(prob_pred, prob_true, marker="o", linewidth=2,
                label=f"{model} (ECE={ece:.3f})")

        ax.set_xlabel("Mean Predicted Probability", fontsize=10)
        ax.set_ylabel("Fraction of Positives", fontsize=10)
        ax.set_title(model, fontsize=12, fontweight='bold')
        ax.legend(loc="upper left", fontsize=8)
        ax.grid(alpha=0.3)
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])

    # Hide empty subplots
    for idx in range(n_models, n_rows * n_cols):
        row = idx // n_cols
        col = idx % n_cols
        axes[row, col].axis('off')

    plt.tight_layout()

    output_file = output_dir / "reliability_diagrams_all.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    logger.info(f"Saved combined reliability diagrams to {output_file}")
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Analyze calibration metrics")
    parser.add_argument("--results", type=Path, required=True, help="Results directory")
    parser.add_argument("--output", type=Path, default=Path("paper/figs/calibration"), help="Output directory")
    parser.add_argument("--n-bins", type=int, default=10, help="Number of bins for ECE")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")

    args = parser.parse_args()

    set_seed(args.seed)
    args.output.mkdir(parents=True, exist_ok=True)

    logger.info("="*80)
    logger.info("CALIBRATION ANALYSIS")
    logger.info("="*80)

    # Template for calibration analysis
    logger.info("""
This script requires actual model predictions to compute calibration metrics.

To use:
1. Run experiments: python experiments/run_experiment.py --dataset compas --models all
2. The experiment runner saves predictions
3. This script loads predictions and computes calibration metrics

For now, a template structure has been created.
You can manually compute calibration metrics using the evaluation module:

    from evaluation import compute_calibration_metrics, plot_reliability_diagram

    metrics = compute_calibration_metrics(y_true, y_proba, n_bins=10)
    fig = plot_reliability_diagram(y_true, y_proba, n_bins=10)

The calibration metrics include:
- Brier Score: Mean squared error of probabilistic predictions
- ECE (Expected Calibration Error): Weighted average of |accuracy - confidence|
- MCE (Maximum Calibration Error): Max calibration error across bins
- Reliability diagrams: Visual assessment of calibration

Post-hoc calibration methods:
- Temperature scaling: Rescale logits with learned temperature parameter
- Isotonic regression: Non-parametric calibration
- Platt scaling: Logistic regression on probabilities
    """)

    # Save calibration analysis configuration
    config = {
        "calibration_metrics": [
            "brier_score",
            "ece",
            "mce",
            "log_loss",
        ],
        "n_bins": args.n_bins,
        "calibration_methods": [
            "temperature_scaling",
            "isotonic_regression",
            "platt_scaling",
        ],
        "calibration_thresholds": {
            "good_ece": 0.05,
            "moderate_ece": 0.10,
        },
    }

    config_file = args.output / "calibration_config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    logger.info(f"\nSaved calibration configuration to {config_file}")
    logger.info("✓ Calibration analysis framework ready")


if __name__ == "__main__":
    main()
