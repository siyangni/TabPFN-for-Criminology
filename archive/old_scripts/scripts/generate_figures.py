"""
Master script for generating all publication-quality figures.

This script:
1. Loads experimental results from JSON files
2. Generates ROC/PR curves, reliability diagrams, fairness plots
3. Creates comparison figures across models
4. Saves all figures to paper/figs/ with publication settings (300 DPI)

Usage:
    python scripts/generate_figures.py --results experiments/results --output paper/figs
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import json
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
from sklearn.metrics import roc_curve, precision_recall_curve, auc

from evaluation import (
    plot_reliability_diagram,
    compute_calibration_metrics,
)
from utils import set_seed, setup_logger

logger = setup_logger("generate_figures")

# Set publication-quality plotting defaults
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 16,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans'],
})

sns.set_palette("colorblind")


def load_results(results_dir: Path, dataset: str) -> Dict:
    """Load all model results for a dataset."""

    results = {}
    dataset_dir = results_dir / dataset

    if not dataset_dir.exists():
        logger.warning(f"Results directory not found: {dataset_dir}")
        return results

    # Look for result JSON files
    for json_file in dataset_dir.glob("**/*.json"):
        if "config" in json_file.name or "versions" in json_file.name:
            continue

        try:
            with open(json_file, 'r') as f:
                data = json.load(f)

            # Extract model name from file path or data
            model_name = json_file.stem
            if "model" in data:
                model_name = data["model"]
            elif "model_name" in data:
                model_name = data["model_name"]

            results[model_name] = data
            logger.info(f"Loaded results for {model_name} from {json_file.name}")

        except Exception as e:
            logger.warning(f"Could not load {json_file}: {e}")

    return results


def plot_roc_curves(
    results: Dict,
    output_dir: Path,
    title: str = "ROC Curves",
):
    """Plot ROC curves for all models."""

    fig, ax = plt.subplots(figsize=(8, 8))

    for model_name, data in results.items():
        if "roc_curve" in data:
            fpr = data["roc_curve"]["fpr"]
            tpr = data["roc_curve"]["tpr"]
            auroc = data["metrics"]["auroc"]

            ax.plot(fpr, tpr, linewidth=2, label=f"{model_name} (AUC={auroc:.3f})")

    # Plot diagonal
    ax.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Chance')

    ax.set_xlabel('False Positive Rate', fontsize=12)
    ax.set_ylabel('True Positive Rate', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(alpha=0.3)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])

    output_file = output_dir / "roc_curves.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    logger.info(f"Saved ROC curves to {output_file}")
    plt.close()


def plot_pr_curves(
    results: Dict,
    output_dir: Path,
    title: str = "Precision-Recall Curves",
):
    """Plot Precision-Recall curves for all models."""

    fig, ax = plt.subplots(figsize=(8, 8))

    for model_name, data in results.items():
        if "pr_curve" in data:
            precision = data["pr_curve"]["precision"]
            recall = data["pr_curve"]["recall"]
            auprc = data["metrics"]["auprc"]

            ax.plot(recall, precision, linewidth=2,
                   label=f"{model_name} (AUC={auprc:.3f})")

    ax.set_xlabel('Recall', fontsize=12)
    ax.set_ylabel('Precision', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(alpha=0.3)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])

    output_file = output_dir / "pr_curves.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    logger.info(f"Saved PR curves to {output_file}")
    plt.close()


def plot_performance_comparison(
    results: Dict,
    output_dir: Path,
    metrics: List[str] = ["auroc", "auprc", "f1", "accuracy"],
):
    """Plot performance metrics comparison across models."""

    models = list(results.keys())
    n_metrics = len(metrics)

    fig, axes = plt.subplots(1, n_metrics, figsize=(5*n_metrics, 6))

    if n_metrics == 1:
        axes = [axes]

    for idx, metric in enumerate(metrics):
        ax = axes[idx]

        values = []
        for model in models:
            if "metrics" in results[model] and metric in results[model]["metrics"]:
                values.append(results[model]["metrics"][metric])
            else:
                values.append(np.nan)

        # Create bar chart
        bars = ax.barh(models, values, color='steelblue', alpha=0.7)

        # Color code based on performance
        if metric in ["auroc", "auprc", "f1", "accuracy"]:
            # Higher is better
            colors = ['green' if v > 0.75 else 'orange' if v > 0.65 else 'red'
                     for v in values]
        else:
            # For error metrics (lower is better)
            colors = ['green' if v < 0.05 else 'orange' if v < 0.10 else 'red'
                     for v in values]

        for bar, color in zip(bars, colors):
            if not np.isnan(bar.get_width()):
                bar.set_color(color)

        ax.set_xlabel(metric.upper(), fontsize=12)
        ax.set_title(f'{metric.upper()} Comparison', fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3, axis='x')
        ax.set_xlim([0, 1])

        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, values)):
            if not np.isnan(value):
                ax.text(value + 0.01, i, f'{value:.3f}',
                       va='center', fontsize=9)

    plt.tight_layout()

    output_file = output_dir / "performance_comparison.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    logger.info(f"Saved performance comparison to {output_file}")
    plt.close()


def plot_calibration_comparison(
    results: Dict,
    output_dir: Path,
):
    """Plot calibration metrics comparison across models."""

    models = list(results.keys())
    metrics_names = ['brier_score', 'ece', 'mce']

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for idx, metric_name in enumerate(metrics_names):
        ax = axes[idx]

        values = []
        for model in models:
            if "calibration" in results[model] and metric_name in results[model]["calibration"]:
                values.append(results[model]["calibration"][metric_name])
            else:
                values.append(np.nan)

        bars = ax.barh(models, values, color='steelblue', alpha=0.7)

        # Color code: green if good, orange if moderate, red if poor
        colors = []
        for v in values:
            if np.isnan(v):
                colors.append('gray')
            elif v < 0.05:
                colors.append('green')
            elif v < 0.10:
                colors.append('orange')
            else:
                colors.append('red')

        for bar, color in zip(bars, colors):
            bar.set_color(color)

        ax.set_xlabel(metric_name.replace('_', ' ').title(), fontsize=12)
        ax.set_title(f'{metric_name.replace("_", " ").title()} Comparison',
                    fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3, axis='x')

        # Add reference lines for ECE
        if metric_name == 'ece':
            ax.axvline(x=0.05, color='green', linestyle='--', alpha=0.5,
                      label='Good (<0.05)')
            ax.axvline(x=0.10, color='orange', linestyle='--', alpha=0.5,
                      label='Moderate (<0.10)')
            ax.legend(fontsize=8)

        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, values)):
            if not np.isnan(value):
                ax.text(value + 0.005, i, f'{value:.3f}',
                       va='center', fontsize=9)

    plt.tight_layout()

    output_file = output_dir / "calibration_comparison.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    logger.info(f"Saved calibration comparison to {output_file}")
    plt.close()


def plot_fairness_comparison(
    results: Dict,
    output_dir: Path,
    sensitive_attr: str = "race",
):
    """Plot fairness metrics comparison across models."""

    models = list(results.keys())
    metrics_names = ['demographic_parity_difference', 'equalized_odds_difference']
    labels = ['Demographic Parity Difference', 'Equalized Odds Difference']

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    for idx, (metric_name, label) in enumerate(zip(metrics_names, labels)):
        ax = axes[idx]

        values = []
        for model in models:
            if "fairness" in results[model] and sensitive_attr in results[model]["fairness"]:
                fairness_data = results[model]["fairness"][sensitive_attr]
                if metric_name in fairness_data:
                    values.append(abs(fairness_data[metric_name]))
                else:
                    values.append(np.nan)
            else:
                values.append(np.nan)

        bars = ax.barh(models, values, color='steelblue', alpha=0.7)

        # Color code based on fairness thresholds
        colors = []
        for v in values:
            if np.isnan(v):
                colors.append('gray')
            elif v < 0.05:
                colors.append('green')
            elif v < 0.10:
                colors.append('orange')
            else:
                colors.append('red')

        for bar, color in zip(bars, colors):
            bar.set_color(color)

        ax.set_xlabel(label, fontsize=12)
        ax.set_title(f'{label} ({sensitive_attr})', fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3, axis='x')

        # Add reference lines
        ax.axvline(x=0.05, color='green', linestyle='--', alpha=0.5,
                  label='Fair (<0.05)')
        ax.axvline(x=0.10, color='orange', linestyle='--', alpha=0.5,
                  label='Moderate (<0.10)')
        ax.legend(fontsize=8)

        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, values)):
            if not np.isnan(value):
                ax.text(value + 0.005, i, f'{value:.3f}',
                       va='center', fontsize=9)

    plt.tight_layout()

    output_file = output_dir / f"fairness_comparison_{sensitive_attr}.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    logger.info(f"Saved fairness comparison to {output_file}")
    plt.close()


def generate_results_table(
    results: Dict,
    output_dir: Path,
    metrics: List[str] = ["auroc", "auprc", "f1", "brier_score", "ece"],
):
    """Generate LaTeX table of results."""

    # Prepare data
    rows = []
    for model_name, data in results.items():
        row = {"Model": model_name}

        # Add performance metrics
        if "metrics" in data:
            for metric in metrics:
                if metric in data["metrics"]:
                    row[metric.upper()] = f"{data['metrics'][metric]:.3f}"
                elif "calibration" in data and metric in data["calibration"]:
                    row[metric.upper()] = f"{data['calibration'][metric]:.3f}"

        rows.append(row)

    df = pd.DataFrame(rows)

    # Save as CSV
    csv_file = output_dir / "results_table.csv"
    df.to_csv(csv_file, index=False)
    logger.info(f"Saved results table to {csv_file}")

    # Save as LaTeX
    latex_file = output_dir / "results_table.tex"
    latex_str = df.to_latex(index=False, float_format="%.3f",
                            caption="Model Performance Comparison",
                            label="tab:results")

    with open(latex_file, 'w') as f:
        f.write(latex_str)

    logger.info(f"Saved LaTeX table to {latex_file}")

    return df


def main():
    parser = argparse.ArgumentParser(description="Generate all publication figures")
    parser.add_argument("--results", type=Path, default=Path("experiments/results"),
                       help="Results directory")
    parser.add_argument("--output", type=Path, default=Path("paper/figs"),
                       help="Output directory for figures")
    parser.add_argument("--dataset", type=str, default="compas",
                       help="Dataset name")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")

    args = parser.parse_args()

    set_seed(args.seed)
    args.output.mkdir(parents=True, exist_ok=True)

    logger.info("="*80)
    logger.info("FIGURE GENERATION")
    logger.info("="*80)
    logger.info(f"Results directory: {args.results}")
    logger.info(f"Output directory: {args.output}")
    logger.info(f"Dataset: {args.dataset}")

    # Load results
    logger.info("\nLoading results...")
    results = load_results(args.results, args.dataset)

    if not results:
        logger.warning("No results found. Please run experiments first.")
        logger.info("\nTo run experiments:")
        logger.info(f"  python experiments/run_experiment.py --dataset {args.dataset} --models all")
        return

    logger.info(f"Loaded results for {len(results)} models: {', '.join(results.keys())}")

    # Generate figures
    logger.info("\nGenerating figures...")

    # 1. ROC curves
    if any("roc_curve" in data for data in results.values()):
        logger.info("  - ROC curves")
        plot_roc_curves(results, args.output, title=f"ROC Curves - {args.dataset.upper()}")

    # 2. PR curves
    if any("pr_curve" in data for data in results.values()):
        logger.info("  - Precision-Recall curves")
        plot_pr_curves(results, args.output, title=f"PR Curves - {args.dataset.upper()}")

    # 3. Performance comparison
    logger.info("  - Performance comparison")
    plot_performance_comparison(results, args.output)

    # 4. Calibration comparison
    if any("calibration" in data for data in results.values()):
        logger.info("  - Calibration comparison")
        plot_calibration_comparison(results, args.output)

    # 5. Fairness comparison
    if any("fairness" in data for data in results.values()):
        logger.info("  - Fairness comparison")
        for sensitive_attr in ["race", "sex", "age_cat"]:
            if any(sensitive_attr in data.get("fairness", {}) for data in results.values()):
                plot_fairness_comparison(results, args.output, sensitive_attr)

    # 6. Results table
    logger.info("  - Results table")
    generate_results_table(results, args.output)

    logger.info("\n" + "="*80)
    logger.info("FIGURE GENERATION COMPLETE")
    logger.info("="*80)
    logger.info(f"\nAll figures saved to: {args.output}")
    logger.info("\nGenerated files:")
    for fig_file in sorted(args.output.glob("*.png")):
        logger.info(f"  - {fig_file.name}")
    for table_file in sorted(args.output.glob("*.csv")) + sorted(args.output.glob("*.tex")):
        logger.info(f"  - {table_file.name}")


if __name__ == "__main__":
    main()
