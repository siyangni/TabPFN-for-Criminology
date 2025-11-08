"""
Comprehensive fairness analysis for COMPAS and other datasets.

This script:
1. Loads experimental results
2. Computes fairness metrics (Fairlearn & Aequitas)
3. Generates fairness reports and visualizations
4. Saves results for manuscript
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import json
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List

from data import COMPASLoader
from evaluation import compute_fairness_metrics, FairnessAuditor
from utils import set_seed, setup_logger

logger = setup_logger("fairness_analysis")


def load_model_predictions(results_dir: Path, model_name: str) -> Dict:
    """Load model predictions from results."""
    result_files = list(results_dir.glob(f"*{model_name}*.json"))
    if not result_files:
        raise FileNotFoundError(f"No results found for {model_name} in {results_dir}")

    with open(result_files[0], 'r') as f:
        return json.load(f)


def analyze_fairness_single_model(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_proba: np.ndarray,
    sensitive_features: pd.DataFrame,
    model_name: str,
    output_dir: Path,
) -> Dict:
    """Analyze fairness for a single model."""

    logger.info(f"Analyzing fairness for {model_name}...")

    # Compute Fairlearn metrics
    fairness_metrics = compute_fairness_metrics(
        y_true, y_pred, sensitive_features, y_proba
    )

    # Run Aequitas audit
    auditor = FairnessAuditor()
    audit_results = auditor.audit(
        y_true, y_pred, y_proba, sensitive_features,
        reference_groups={'race': 'Caucasian', 'sex': 'Male'}
    )

    # Generate report
    report = auditor.generate_report(
        output_path=output_dir / f"{model_name}_fairness_report.txt"
    )

    # Save metrics
    output_file = output_dir / f"{model_name}_fairness_metrics.json"
    with open(output_file, 'w') as f:
        json.dump(fairness_metrics, f, indent=2, default=str)

    logger.info(f"Saved fairness metrics to {output_file}")

    return fairness_metrics


def plot_fairness_comparison(
    fairness_results: Dict[str, Dict],
    sensitive_attr: str,
    output_dir: Path,
):
    """Plot fairness metrics comparison across models."""

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    models = list(fairness_results.keys())

    # Plot 1: Equalized Odds Difference
    eod_values = [
        fairness_results[model][sensitive_attr]['equalized_odds_difference']
        for model in models
    ]

    axes[0].barh(models, eod_values, color=['red' if v > 0.1 else 'green' for v in eod_values])
    axes[0].axvline(x=0.1, color='orange', linestyle='--', label='Fairness threshold (0.1)')
    axes[0].set_xlabel('Equalized Odds Difference', fontsize=12)
    axes[0].set_title(f'Equalized Odds Difference by {sensitive_attr}', fontsize=14, fontweight='bold')
    axes[0].legend()
    axes[0].grid(alpha=0.3, axis='x')

    # Plot 2: Demographic Parity Difference
    dpd_values = [
        fairness_results[model][sensitive_attr]['demographic_parity_difference']
        for model in models
    ]

    axes[1].barh(models, dpd_values, color=['red' if v > 0.1 else 'green' for v in dpd_values])
    axes[1].axvline(x=0.1, color='orange', linestyle='--', label='Fairness threshold (0.1)')
    axes[1].set_xlabel('Demographic Parity Difference', fontsize=12)
    axes[1].set_title(f'Demographic Parity Difference by {sensitive_attr}', fontsize=14, fontweight='bold')
    axes[1].legend()
    axes[1].grid(alpha=0.3, axis='x')

    plt.tight_layout()

    output_file = output_dir / f"fairness_comparison_{sensitive_attr}.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    logger.info(f"Saved fairness comparison plot to {output_file}")
    plt.close()


def plot_group_performance(
    fairness_results: Dict[str, Dict],
    sensitive_attr: str,
    output_dir: Path,
):
    """Plot performance metrics by group."""

    # Extract group metrics from first model (assume all models have same groups)
    first_model = list(fairness_results.keys())[0]
    group_metrics = fairness_results[first_model][sensitive_attr]['group_metrics']

    groups = list(group_metrics.keys())
    metrics = ['accuracy', 'precision', 'recall']
    models = list(fairness_results.keys())

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    x = np.arange(len(groups))
    width = 0.8 / len(models)

    for metric_idx, metric in enumerate(metrics):
        ax = axes[metric_idx]

        for model_idx, model in enumerate(models):
            values = [
                fairness_results[model][sensitive_attr]['group_metrics'][group][metric]
                for group in groups
            ]

            offset = (model_idx - len(models)/2) * width + width/2
            ax.bar(x + offset, values, width, label=model, alpha=0.8)

        ax.set_ylabel(metric.capitalize(), fontsize=12)
        ax.set_title(f'{metric.capitalize()} by {sensitive_attr} Group', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(groups, rotation=45, ha='right')
        ax.legend()
        ax.grid(alpha=0.3, axis='y')
        ax.set_ylim([0, 1])

    plt.tight_layout()

    output_file = output_dir / f"group_performance_{sensitive_attr}.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    logger.info(f"Saved group performance plot to {output_file}")
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Analyze fairness metrics")
    parser.add_argument("--results", type=Path, required=True, help="Results directory")
    parser.add_argument("--dataset", type=str, default="compas", help="Dataset name")
    parser.add_argument("--output", type=Path, default=Path("paper/figs/fairness"), help="Output directory")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")

    args = parser.parse_args()

    set_seed(args.seed)
    args.output.mkdir(parents=True, exist_ok=True)

    logger.info("="*80)
    logger.info("FAIRNESS ANALYSIS")
    logger.info("="*80)

    # Load dataset to get sensitive features
    if args.dataset == "compas":
        from data import COMPASLoader
        loader = COMPASLoader(Path("data"), task="two_year")

        # Load processed data
        df = loader.preprocess(loader.load_raw())
        X, y, sensitive = loader.get_X_y_sensitive(df)

        logger.info(f"Loaded COMPAS data: {len(X)} samples")
        logger.info(f"Sensitive features: {sensitive.columns.tolist()}")

    else:
        logger.error(f"Dataset {args.dataset} not supported for fairness analysis yet")
        return

    # For now, create a comprehensive fairness report template
    # In practice, you would load actual model predictions here

    logger.info("\n" + "="*80)
    logger.info("FAIRNESS ANALYSIS SUMMARY")
    logger.info("="*80)
    logger.info("""
This script requires actual model predictions to compute fairness metrics.

To use:
1. Run experiments: python experiments/run_experiment.py --dataset compas --models all
2. The experiment runner saves predictions
3. This script loads predictions and computes fairness metrics

For now, a template structure has been created.
You can manually compute fairness metrics using the evaluation module:

    from evaluation import compute_fairness_metrics
    fairness = compute_fairness_metrics(y_true, y_pred, sensitive_features, y_proba)

The fairness metrics include:
- Demographic Parity Difference (DPD)
- Equalized Odds Difference (EOD)
- Group-specific TPR, FPR, accuracy, precision, recall
- Fairness audit via Aequitas
    """)

    # Save fairness analysis configuration
    config = {
        "dataset": args.dataset,
        "sensitive_attributes": sensitive.columns.tolist(),
        "fairness_metrics": [
            "demographic_parity_difference",
            "equalized_odds_difference",
            "tpr_ratio",
            "fpr_ratio",
        ],
        "reference_groups": {
            "race": "Caucasian",
            "sex": "Male",
        },
        "fairness_threshold": 0.1,
    }

    config_file = args.output / "fairness_config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    logger.info(f"\nSaved fairness configuration to {config_file}")
    logger.info("✓ Fairness analysis framework ready")


if __name__ == "__main__":
    main()
