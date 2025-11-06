#!/usr/bin/env python
"""Basic fairness analysis using standard libraries (no fairlearn/aequitas required).

Computes group-specific performance metrics and fairness measures for COMPAS models.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix
)
import json
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.data import COMPASLoader

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10

print("="*80)
print("BASIC FAIRNESS ANALYSIS FOR COMPAS RECIDIVISM MODELS")
print("="*80)

# Load COMPAS data
print("\n[1/4] Loading COMPAS dataset...")
loader = COMPASLoader(Path("data"), task="two_year", random_state=42)
X, y = loader.load_and_prepare(include_compas_score=False)

# Load raw data to get sensitive features
df_raw = loader.preprocess(loader.load_raw())
print(f"✓ Loaded {len(X)} samples")

# Get sensitive attributes (race)
# Map COMPAS dataset indices to the filtered dataset
race = df_raw['race'].values

# Load predictions
print("\n[2/4] Loading model predictions...")
predictions_file = Path("experiments/predictions/compas_predictions.npz")
data = np.load(predictions_file)

y_test = data['y_test']
predictions = {
    "Logistic Regression": data['logistic_regression_proba'],
    "XGBoost": data['xgboost_proba'],
    "LightGBM": data['lightgbm_proba'],
    "CatBoost": data['catboost_proba']
}

# Note: We need to map test indices to race information
# For this analysis, we'll use the test split from the same random seed
from sklearn.model_selection import train_test_split
_, X_test_idx, _, y_test_check = train_test_split(
    np.arange(len(X)), y, test_size=0.2, random_state=42, stratify=y
)

# Get race for test samples
race_test = race[X_test_idx]
print(f"✓ Loaded predictions for {len(predictions)} models")

# Analyze fairness metrics
print("\n[3/4] Computing fairness metrics...")

def compute_fairness_metrics(y_true, y_pred, y_pred_proba, sensitive_attr):
    """Compute fairness metrics for each group."""
    unique_groups = np.unique(sensitive_attr)
    results = []

    for group in unique_groups:
        group_mask = sensitive_attr == group
        n_samples = np.sum(group_mask)

        if n_samples < 10:  # Skip groups with too few samples
            continue

        # Get group-specific data
        y_true_group = y_true[group_mask]
        y_pred_group = y_pred[group_mask]
        y_pred_proba_group = y_pred_proba[group_mask]

        # Compute metrics
        tn, fp, fn, tp = confusion_matrix(y_true_group, y_pred_group).ravel()

        metrics = {
            'group': group,
            'n_samples': n_samples,
            'base_rate': np.mean(y_true_group),  # P(Y=1)
            'selection_rate': np.mean(y_pred_group),  # P(Ŷ=1)
            'accuracy': accuracy_score(y_true_group, y_pred_group),
            'precision': precision_score(y_true_group, y_pred_group, zero_division=0),
            'recall': recall_score(y_true_group, y_pred_group, zero_division=0),
            'f1': f1_score(y_true_group, y_pred_group, zero_division=0),
            'fpr': fp / (fp + tn) if (fp + tn) > 0 else 0,  # False Positive Rate
            'fnr': fn / (fn + tp) if (fn + tp) > 0 else 0,  # False Negative Rate
            'tpr': recall_score(y_true_group, y_pred_group, zero_division=0),  # True Positive Rate
            'tnr': tn / (tn + fp) if (tn + fp) > 0 else 0,  # True Negative Rate
        }

        # Try to compute AUROC (may fail if only one class present)
        try:
            metrics['auroc'] = roc_auc_score(y_true_group, y_pred_proba_group)
        except:
            metrics['auroc'] = np.nan

        results.append(metrics)

    return pd.DataFrame(results)

# Compute metrics for all models
all_fairness_results = {}

for model_name, y_pred_proba in predictions.items():
    y_pred = (y_pred_proba > 0.5).astype(int)
    df_fairness = compute_fairness_metrics(y_test, y_pred, y_pred_proba, race_test)
    all_fairness_results[model_name] = df_fairness
    print(f"  ✓ {model_name}")

# Compute fairness disparities
print("\n[4/4] Computing fairness disparities...")

def compute_disparities(df_fairness, reference_group='Caucasian'):
    """Compute disparity ratios relative to reference group."""
    if reference_group not in df_fairness['group'].values:
        reference_group = df_fairness['group'].values[0]

    ref_metrics = df_fairness[df_fairness['group'] == reference_group].iloc[0]

    disparities = []
    for _, row in df_fairness.iterrows():
        if row['group'] == reference_group:
            continue

        disp = {
            'group': row['group'],
            'demographic_parity': row['selection_rate'] / ref_metrics['selection_rate'] if ref_metrics['selection_rate'] > 0 else np.nan,
            'equalized_odds_fpr': row['fpr'] / ref_metrics['fpr'] if ref_metrics['fpr'] > 0 else np.nan,
            'equalized_odds_tpr': row['tpr'] / ref_metrics['tpr'] if ref_metrics['tpr'] > 0 else np.nan,
            'accuracy_parity': row['accuracy'] / ref_metrics['accuracy'] if ref_metrics['accuracy'] > 0 else np.nan,
        }
        disparities.append(disp)

    return pd.DataFrame(disparities) if disparities else pd.DataFrame()

# Create output directory
output_dir = Path("analysis/fairness")
output_dir.mkdir(parents=True, exist_ok=True)

# Print and save results
print("\n" + "="*80)
print("GROUP-SPECIFIC PERFORMANCE METRICS")
print("="*80)

for model_name, df_fairness in all_fairness_results.items():
    print(f"\n{model_name}:")
    print("-" * 80)
    print(df_fairness[['group', 'n_samples', 'accuracy', 'precision', 'recall', 'fpr', 'fnr']].to_string(index=False))

    # Save to CSV
    df_fairness.to_csv(output_dir / f"{model_name.lower().replace(' ', '_')}_fairness.csv", index=False)

print("\n" + "="*80)
print("FAIRNESS DISPARITIES (ratio to Caucasian group)")
print("="*80)

disparity_results = {}
for model_name, df_fairness in all_fairness_results.items():
    df_disp = compute_disparities(df_fairness, reference_group='Caucasian')
    if not df_disp.empty:
        disparity_results[model_name] = df_disp
        print(f"\n{model_name}:")
        print("-" * 80)
        print(df_disp.to_string(index=False))

        # Save to CSV
        df_disp.to_csv(output_dir / f"{model_name.lower().replace(' ', '_')}_disparities.csv", index=False)

# Generate visualizations
print("\n[5/5] Generating fairness visualizations...")

# 1. False Positive Rate by Race
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
axes = axes.ravel()

for idx, (model_name, df_fairness) in enumerate(all_fairness_results.items()):
    ax = axes[idx]

    # Create grouped bar chart
    groups = df_fairness['group'].values
    fpr = df_fairness['fpr'].values
    fnr = df_fairness['fnr'].values

    x = np.arange(len(groups))
    width = 0.35

    bars1 = ax.bar(x - width/2, fpr, width, label='False Positive Rate', alpha=0.8)
    bars2 = ax.bar(x + width/2, fnr, width, label='False Negative Rate', alpha=0.8)

    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.3f}', ha='center', va='bottom', fontsize=8)

    ax.set_ylabel('Rate', fontweight='bold')
    ax.set_title(f'{model_name}', fontweight='bold', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(groups, rotation=30, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, max(max(fpr), max(fnr)) * 1.2)

plt.suptitle('False Positive and False Negative Rates by Race',
             fontweight='bold', fontsize=15, y=0.995)
plt.tight_layout()
plt.savefig(output_dir / "error_rates_by_race.png", dpi=300, bbox_inches='tight')
plt.savefig(output_dir / "error_rates_by_race.pdf", bbox_inches='tight')
plt.close()

# 2. Accuracy by Race
fig, ax = plt.subplots(figsize=(12, 6))

for model_name, df_fairness in all_fairness_results.items():
    groups = df_fairness['group'].values
    accuracy = df_fairness['accuracy'].values
    ax.plot(groups, accuracy, marker='o', linewidth=2.5, markersize=10,
            label=model_name)

ax.set_xlabel('Race', fontweight='bold', fontsize=12)
ax.set_ylabel('Accuracy', fontweight='bold', fontsize=12)
ax.set_title('Model Accuracy by Race', fontweight='bold', fontsize=14)
ax.legend(frameon=True, shadow=True)
ax.grid(True, alpha=0.3)
ax.set_ylim(0.6, 0.8)

plt.tight_layout()
plt.savefig(output_dir / "accuracy_by_race.png", dpi=300, bbox_inches='tight')
plt.savefig(output_dir / "accuracy_by_race.pdf", bbox_inches='tight')
plt.close()

print(f"✓ Saved error rates plot to {output_dir}/error_rates_by_race.png")
print(f"✓ Saved accuracy plot to {output_dir}/accuracy_by_race.png")

# Save summary JSON
summary = {}
for model_name, df_fairness in all_fairness_results.items():
    summary[model_name] = {
        'group_metrics': df_fairness.to_dict(orient='records'),
        'disparities': disparity_results.get(model_name, pd.DataFrame()).to_dict(orient='records')
    }

with open(output_dir / "fairness_summary.json", 'w') as f:
    json.dump(summary, f, indent=2, default=str)

print(f"✓ Saved fairness summary to {output_dir}/fairness_summary.json")

print("\n" + "="*80)
print("KEY FINDINGS")
print("="*80)

# Identify most concerning disparities
print("\nMost Concerning Disparities:")
for model_name, df_disp in disparity_results.items():
    if not df_disp.empty:
        # Find largest disparity in FPR
        max_fpr_disp = df_disp['equalized_odds_fpr'].max()
        max_fpr_group = df_disp.loc[df_disp['equalized_odds_fpr'].idxmax(), 'group']
        print(f"  {model_name}:")
        print(f"    - Largest FPR disparity: {max_fpr_disp:.2f}x ({max_fpr_group} vs Caucasian)")

print("\n" + "="*80)
print("Note: Fairness ratios close to 1.0 indicate parity between groups.")
print("Ratios > 1.0 indicate higher rates for the comparison group.")
print("Ratios < 1.0 indicate lower rates for the comparison group.")
print("="*80)
