#!/usr/bin/env python
"""Generate all publication-quality figures for the paper.

This script trains models using best hyperparameters found during optimization,
then generates ROC curves, PR curves, and calibration plots.
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    roc_curve, auc, precision_recall_curve,
    average_precision_score, brier_score_loss
)
from sklearn.calibration import calibration_curve
from sklearn.linear_model import LogisticRegression
import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostClassifier
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.data import COMPASLoader
from src.utils.seed import set_seed

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

# Set seed
set_seed(42)

# Create output directory
output_dir = Path("paper/figs")
output_dir.mkdir(parents=True, exist_ok=True)

print("="*80)
print("GENERATING PUBLICATION FIGURES")
print("="*80)

# Load COMPAS data
print("\n[1/6] Loading COMPAS dataset...")
loader = COMPASLoader(Path("data"), task="two_year", random_state=42)
X, y = loader.load_and_prepare(include_compas_score=False)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"✓ Loaded {len(X)} samples ({len(X_train)} train, {len(X_test)} test)")

# Load best hyperparameters
print("\n[2/6] Loading best hyperparameters...")
results_dir = Path("experiments/results/compas")
result_files = sorted(results_dir.glob("*.json"))

best_params = {}
for file_path in result_files:
    with open(file_path, 'r') as f:
        data = json.load(f)
    for model_name, model_data in data.items():
        if "best_params" in model_data:
            best_params[model_name] = model_data["best_params"]
            print(f"  ✓ {model_name.upper()}")

# Train models with best hyperparameters
print("\n[3/6] Training models with best hyperparameters...")
models = {}
predictions = {}

# Logistic Regression
print("  Training Logistic Regression...")
lr = LogisticRegression(random_state=42, max_iter=1000)
lr.fit(X_train, y_train)
models["Logistic Regression"] = lr
predictions["Logistic Regression"] = lr.predict_proba(X_test)[:, 1]
print("  ✓ Logistic Regression")

# XGBoost
if "xgboost" in best_params:
    print("  Training XGBoost...")
    params = best_params["xgboost"].copy()
    params.update({
        'random_state': 42,
        'objective': 'binary:logistic',
        'eval_metric': 'logloss',
        'use_label_encoder': False,
        'tree_method': 'hist'
    })
    xgb_model = xgb.XGBClassifier(**params)
    xgb_model.fit(X_train, y_train, verbose=False)
    models["XGBoost"] = xgb_model
    predictions["XGBoost"] = xgb_model.predict_proba(X_test)[:, 1]
    print("  ✓ XGBoost")

# LightGBM
if "lightgbm" in best_params:
    print("  Training LightGBM...")
    params = best_params["lightgbm"].copy()
    params.update({
        'random_state': 42,
        'objective': 'binary',
        'metric': 'binary_logloss',
        'verbosity': -1
    })
    lgb_model = lgb.LGBMClassifier(**params)
    lgb_model.fit(X_train, y_train)
    models["LightGBM"] = lgb_model
    predictions["LightGBM"] = lgb_model.predict_proba(X_test)[:, 1]
    print("  ✓ LightGBM")

# CatBoost
if "catboost" in best_params:
    print("  Training CatBoost...")
    params = best_params["catboost"].copy()
    params.update({
        'random_state': 42,
        'loss_function': 'Logloss',
        'verbose': False
    })
    cat_model = CatBoostClassifier(**params)
    cat_model.fit(X_train, y_train, verbose=False)
    models["CatBoost"] = cat_model
    predictions["CatBoost"] = cat_model.predict_proba(X_test)[:, 1]
    print("  ✓ CatBoost")

# Generate ROC curves
print("\n[4/6] Generating ROC curves...")
fig, ax = plt.subplots(figsize=(8, 8))

# Color palette
colors = {
    "Logistic Regression": "#e377c2",  # Pink
    "XGBoost": "#17becf",              # Cyan
    "LightGBM": "#bcbd22",             # Yellow-green
    "CatBoost": "#ff7f0e"              # Orange
}

# Plot ROC curve for each model
roc_data = {}
for model_name, y_pred_proba in predictions.items():
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    roc_auc = auc(fpr, tpr)
    roc_data[model_name] = {'fpr': fpr, 'tpr': tpr, 'auc': roc_auc}

    ax.plot(fpr, tpr, color=colors[model_name], lw=2.5,
            label=f'{model_name} (AUC = {roc_auc:.4f})')

# Plot diagonal reference line
ax.plot([0, 1], [0, 1], 'k--', lw=1.5, alpha=0.3, label='Random Classifier')

# Formatting
ax.set_xlim([-0.02, 1.02])
ax.set_ylim([-0.02, 1.02])
ax.set_xlabel('False Positive Rate', fontweight='bold')
ax.set_ylabel('True Positive Rate', fontweight='bold')
ax.set_title('ROC Curves: COMPAS Recidivism Prediction', fontweight='bold', fontsize=15)
ax.legend(loc='lower right', frameon=True, shadow=True)
ax.grid(True, alpha=0.3)
ax.set_aspect('equal')

plt.tight_layout()
plt.savefig(output_dir / "roc_curves.png", dpi=300, bbox_inches='tight')
plt.savefig(output_dir / "roc_curves.pdf", bbox_inches='tight')
plt.close()
print(f"✓ Saved ROC curves to {output_dir}/roc_curves.png")

# Generate Precision-Recall curves
print("\n[5/6] Generating Precision-Recall curves...")
fig, ax = plt.subplots(figsize=(8, 8))

# Plot PR curve for each model
pr_data = {}
for model_name, y_pred_proba in predictions.items():
    precision, recall, _ = precision_recall_curve(y_test, y_pred_proba)
    avg_precision = average_precision_score(y_test, y_pred_proba)
    pr_data[model_name] = {'precision': precision, 'recall': recall, 'ap': avg_precision}

    ax.plot(recall, precision, color=colors[model_name], lw=2.5,
            label=f'{model_name} (AP = {avg_precision:.4f})')

# Plot baseline (random classifier)
baseline = y_test.mean()
ax.plot([0, 1], [baseline, baseline], 'k--', lw=1.5, alpha=0.3,
        label=f'Random Classifier (AP = {baseline:.4f})')

# Formatting
ax.set_xlim([-0.02, 1.02])
ax.set_ylim([-0.02, 1.02])
ax.set_xlabel('Recall', fontweight='bold')
ax.set_ylabel('Precision', fontweight='bold')
ax.set_title('Precision-Recall Curves: COMPAS Recidivism Prediction',
             fontweight='bold', fontsize=15)
ax.legend(loc='lower left', frameon=True, shadow=True)
ax.grid(True, alpha=0.3)
ax.set_aspect('equal')

plt.tight_layout()
plt.savefig(output_dir / "pr_curves.png", dpi=300, bbox_inches='tight')
plt.savefig(output_dir / "pr_curves.pdf", bbox_inches='tight')
plt.close()
print(f"✓ Saved PR curves to {output_dir}/pr_curves.png")

# Generate calibration plots (reliability diagrams)
print("\n[6/6] Generating calibration plots...")
fig, axes = plt.subplots(2, 2, figsize=(14, 12))
axes = axes.ravel()

for idx, (model_name, y_pred_proba) in enumerate(predictions.items()):
    ax = axes[idx]

    # Compute calibration curve
    fraction_of_positives, mean_predicted_value = calibration_curve(
        y_test, y_pred_proba, n_bins=10, strategy='uniform'
    )

    # Plot calibration curve
    ax.plot(mean_predicted_value, fraction_of_positives, 's-',
            color=colors[model_name], lw=2.5, markersize=8,
            label=f'{model_name}')

    # Plot perfect calibration line
    ax.plot([0, 1], [0, 1], 'k--', lw=1.5, alpha=0.3, label='Perfect Calibration')

    # Compute Brier score
    brier = brier_score_loss(y_test, y_pred_proba)

    # Formatting
    ax.set_xlim([-0.02, 1.02])
    ax.set_ylim([-0.02, 1.02])
    ax.set_xlabel('Mean Predicted Probability', fontweight='bold')
    ax.set_ylabel('Fraction of Positives', fontweight='bold')
    ax.set_title(f'{model_name}\n(Brier Score = {brier:.4f})',
                 fontweight='bold', fontsize=13)
    ax.legend(loc='upper left', frameon=True)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')

plt.suptitle('Calibration Plots: COMPAS Recidivism Prediction',
             fontweight='bold', fontsize=16, y=1.00)
plt.tight_layout()
plt.savefig(output_dir / "calibration_plots.png", dpi=300, bbox_inches='tight')
plt.savefig(output_dir / "calibration_plots.pdf", bbox_inches='tight')
plt.close()
print(f"✓ Saved calibration plots to {output_dir}/calibration_plots.png")

# Save prediction data for fairness analysis
print("\n[7/6] Saving predictions for fairness analysis...")
predictions_dir = Path("experiments/predictions")
predictions_dir.mkdir(parents=True, exist_ok=True)

np.savez(
    predictions_dir / "compas_predictions.npz",
    y_test=y_test,
    **{f"{name.lower().replace(' ', '_')}_proba": proba
       for name, proba in predictions.items()}
)
print(f"✓ Saved predictions to {predictions_dir}/compas_predictions.npz")

# Print summary
print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print("\nGenerated Files:")
print(f"  • {output_dir}/roc_curves.png")
print(f"  • {output_dir}/roc_curves.pdf")
print(f"  • {output_dir}/pr_curves.png")
print(f"  • {output_dir}/pr_curves.pdf")
print(f"  • {output_dir}/calibration_plots.png")
print(f"  • {output_dir}/calibration_plots.pdf")
print(f"  • {predictions_dir}/compas_predictions.npz")

print("\nModel Performance on Test Set:")
print("-" * 80)
for model_name, y_pred_proba in predictions.items():
    auroc = roc_data[model_name]['auc']
    auprc = pr_data[model_name]['ap']
    brier = brier_score_loss(y_test, y_pred_proba)
    print(f"{model_name:20s} | AUROC: {auroc:.4f} | AUPRC: {auprc:.4f} | Brier: {brier:.4f}")
print("="*80)
