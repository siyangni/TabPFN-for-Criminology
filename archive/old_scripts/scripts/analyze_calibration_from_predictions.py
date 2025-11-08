#!/usr/bin/env python
"""Analyze model calibration using saved predictions."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.calibration import calibration_curve
from sklearn.metrics import brier_score_loss, log_loss
import json

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 11

print("="*80)
print("CALIBRATION ANALYSIS FOR COMPAS RECIDIVISM MODELS")
print("="*80)

# Load predictions
print("\n[1/3] Loading predictions...")
predictions_file = Path("experiments/predictions/compas_predictions.npz")
data = np.load(predictions_file)

y_test = data['y_test']
predictions = {
    "Logistic Regression": data['logistic_regression_proba'],
    "XGBoost": data['xgboost_proba'],
    "LightGBM": data['lightgbm_proba'],
    "CatBoost": data['catboost_proba']
}
print(f"✓ Loaded predictions for {len(predictions)} models on {len(y_test)} test samples")

# Compute calibration metrics
print("\n[2/3] Computing calibration metrics...")

def compute_ece(y_true, y_pred_proba, n_bins=10):
    """Compute Expected Calibration Error."""
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    bin_lowers = bin_boundaries[:-1]
    bin_uppers = bin_boundaries[1:]

    ece = 0.0
    for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
        # Find samples in this bin
        in_bin = np.logical_and(y_pred_proba >= bin_lower, y_pred_proba < bin_upper)
        prop_in_bin = np.mean(in_bin)

        if prop_in_bin > 0:
            accuracy_in_bin = np.mean(y_true[in_bin])
            avg_confidence_in_bin = np.mean(y_pred_proba[in_bin])
            ece += np.abs(accuracy_in_bin - avg_confidence_in_bin) * prop_in_bin

    return ece

def compute_mce(y_true, y_pred_proba, n_bins=10):
    """Compute Maximum Calibration Error."""
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    bin_lowers = bin_boundaries[:-1]
    bin_uppers = bin_boundaries[1:]

    mce = 0.0
    for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
        # Find samples in this bin
        in_bin = np.logical_and(y_pred_proba >= bin_lower, y_pred_proba < bin_upper)
        prop_in_bin = np.mean(in_bin)

        if prop_in_bin > 0:
            accuracy_in_bin = np.mean(y_true[in_bin])
            avg_confidence_in_bin = np.mean(y_pred_proba[in_bin])
            mce = max(mce, np.abs(accuracy_in_bin - avg_confidence_in_bin))

    return mce

# Compute metrics for all models
calibration_metrics = []
for model_name, y_pred_proba in predictions.items():
    brier = brier_score_loss(y_test, y_pred_proba)
    logloss = log_loss(y_test, np.column_stack([1 - y_pred_proba, y_pred_proba]))
    ece = compute_ece(y_test, y_pred_proba, n_bins=10)
    mce = compute_mce(y_test, y_pred_proba, n_bins=10)

    calibration_metrics.append({
        "Model": model_name,
        "Brier Score": brier,
        "Log Loss": logloss,
        "ECE (10 bins)": ece,
        "MCE (10 bins)": mce
    })

    print(f"  ✓ {model_name}")

# Create DataFrame
df = pd.DataFrame(calibration_metrics)
df = df.sort_values("Brier Score")

print("\n" + "="*80)
print("CALIBRATION METRICS")
print("="*80)
print(df.to_string(index=False))
print("="*80)
print("\nNotes:")
print("  • Brier Score: Lower is better (perfect = 0, worst = 1)")
print("  • Log Loss: Lower is better (perfect = 0)")
print("  • ECE: Expected Calibration Error - Lower is better (perfect = 0)")
print("  • MCE: Maximum Calibration Error - Lower is better (perfect = 0)")
print("="*80)

# Save calibration metrics
output_dir = Path("analysis/calibration")
output_dir.mkdir(parents=True, exist_ok=True)

df.to_csv(output_dir / "calibration_metrics.csv", index=False)
df.to_latex(output_dir / "calibration_metrics.tex", index=False, float_format="%.4f")

# Save as JSON
metrics_dict = {}
for _, row in df.iterrows():
    metrics_dict[row['Model']] = {
        'brier_score': float(row['Brier Score']),
        'log_loss': float(row['Log Loss']),
        'ece': float(row['ECE (10 bins)']),
        'mce': float(row['MCE (10 bins)'])
    }

with open(output_dir / "calibration_metrics.json", 'w') as f:
    json.dump(metrics_dict, f, indent=2)

print(f"\n✓ Saved calibration metrics to {output_dir}/calibration_metrics.csv")
print(f"✓ Saved LaTeX table to {output_dir}/calibration_metrics.tex")
print(f"✓ Saved JSON metrics to {output_dir}/calibration_metrics.json")

# Generate detailed reliability diagrams
print("\n[3/3] Generating detailed reliability diagrams...")

fig, axes = plt.subplots(2, 2, figsize=(15, 13))
axes = axes.ravel()

colors = {
    "Logistic Regression": "#e377c2",
    "XGBoost": "#17becf",
    "LightGBM": "#bcbd22",
    "CatBoost": "#ff7f0e"
}

for idx, (model_name, y_pred_proba) in enumerate(predictions.items()):
    ax = axes[idx]

    # Compute calibration curve with more bins for detail
    fraction_of_positives, mean_predicted_value = calibration_curve(
        y_test, y_pred_proba, n_bins=15, strategy='uniform'
    )

    # Plot calibration curve
    ax.plot(mean_predicted_value, fraction_of_positives, 's-',
            color=colors[model_name], lw=2.5, markersize=10,
            label=f'{model_name}', markerfacecolor='white',
            markeredgewidth=2)

    # Plot perfect calibration line
    ax.plot([0, 1], [0, 1], 'k--', lw=2, alpha=0.4, label='Perfect Calibration')

    # Get metrics
    metrics = df[df['Model'] == model_name].iloc[0]
    brier = metrics['Brier Score']
    ece = metrics['ECE (10 bins)']

    # Add histogram of predictions
    ax_hist = ax.twinx()
    ax_hist.hist(y_pred_proba, bins=30, alpha=0.2, color=colors[model_name],
                 edgecolor='black', linewidth=0.5)
    ax_hist.set_ylabel('Count', fontsize=11, color='gray')
    ax_hist.tick_params(axis='y', labelcolor='gray')
    ax_hist.grid(False)

    # Formatting
    ax.set_xlim([-0.02, 1.02])
    ax.set_ylim([-0.02, 1.02])
    ax.set_xlabel('Mean Predicted Probability', fontweight='bold', fontsize=12)
    ax.set_ylabel('Fraction of Positives', fontweight='bold', fontsize=12)
    ax.set_title(f'{model_name}\nBrier: {brier:.4f} | ECE: {ece:.4f}',
                 fontweight='bold', fontsize=13)
    ax.legend(loc='upper left', frameon=True, shadow=True)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')

plt.suptitle('Detailed Calibration Analysis: COMPAS Recidivism Prediction',
             fontweight='bold', fontsize=16, y=0.995)
plt.tight_layout()
plt.savefig(output_dir / "detailed_calibration_plots.png", dpi=300, bbox_inches='tight')
plt.savefig(output_dir / "detailed_calibration_plots.pdf", bbox_inches='tight')
plt.close()

print(f"✓ Saved detailed calibration plots to {output_dir}/detailed_calibration_plots.png")

# Generate ECE comparison plot
fig, ax = plt.subplots(figsize=(10, 6))

models = df['Model'].values
ece_values = df['ECE (10 bins)'].values
mce_values = df['MCE (10 bins)'].values

x = np.arange(len(models))
width = 0.35

bars1 = ax.bar(x - width/2, ece_values, width, label='ECE',
               color=[colors[m] for m in models], alpha=0.7, edgecolor='black')
bars2 = ax.bar(x + width/2, mce_values, width, label='MCE',
               color=[colors[m] for m in models], alpha=0.4, edgecolor='black',
               hatch='//')

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.4f}', ha='center', va='bottom', fontsize=9)

ax.set_ylabel('Calibration Error', fontweight='bold', fontsize=12)
ax.set_title('Expected vs Maximum Calibration Error', fontweight='bold', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(models, rotation=15, ha='right')
ax.legend(frameon=True, shadow=True)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / "calibration_error_comparison.png", dpi=300, bbox_inches='tight')
plt.savefig(output_dir / "calibration_error_comparison.pdf", bbox_inches='tight')
plt.close()

print(f"✓ Saved calibration error comparison to {output_dir}/calibration_error_comparison.png")

print("\n" + "="*80)
print("KEY FINDINGS")
print("="*80)
best_model = df.iloc[0]
print(f"• Best Calibrated Model: {best_model['Model']}")
print(f"  - Brier Score: {best_model['Brier Score']:.4f}")
print(f"  - ECE: {best_model['ECE (10 bins)']:.4f}")
print(f"  - MCE: {best_model['MCE (10 bins)']:.4f}")
print(f"\n• Calibration Quality:")
for _, row in df.iterrows():
    ece = row['ECE (10 bins)']
    if ece < 0.05:
        quality = "Excellent"
    elif ece < 0.10:
        quality = "Good"
    elif ece < 0.15:
        quality = "Fair"
    else:
        quality = "Poor"
    print(f"  - {row['Model']:20s}: ECE = {ece:.4f} ({quality})")
print("="*80)
