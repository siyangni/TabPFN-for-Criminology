"""Quick demonstration experiment on COMPAS data."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import json
import logging

from data import COMPASLoader
from models import LogisticRegressionModel, XGBoostModel
from evaluation import compute_classification_metrics
from utils import set_seed, setup_logger

# Setup
logger = setup_logger("demo_experiment", level=logging.INFO)
set_seed(42)

logger.info("=" * 80)
logger.info("COMPAS Demonstration Experiment")
logger.info("=" * 80)

# Load and prepare data
logger.info("\n1. Loading COMPAS data...")
loader = COMPASLoader(Path("data"), task="two_year", random_state=42)
X, y = loader.load_and_prepare(include_compas_score=False)

logger.info(f"Dataset: {X.shape[0]} samples, {X.shape[1]} features")
logger.info(f"Class distribution: {np.bincount(y)}")
logger.info(f"Positive class rate: {y.mean():.3f}")

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

logger.info(f"Train: {len(X_train)}, Test: {len(X_test)}")

# Run Logistic Regression
logger.info("\n2. Training Logistic Regression (with tuning)...")
logistic = LogisticRegressionModel(
    task_type="classification",
    random_state=42,
    n_trials=10,  # Reduced for demo
    cv_folds=3,
)

logistic.fit(X_train, y_train, tune=True, scale=True, class_weight="balanced")
logger.info(f"Best params: {logistic.best_params}")

y_pred_lr = logistic.predict(X_test)
y_proba_lr = logistic.predict_proba(X_test)[:, 1]

metrics_lr = compute_classification_metrics(y_test, y_pred_lr, y_proba_lr)
logger.info(f"\nLogistic Regression Results:")
logger.info(f"  AUROC: {metrics_lr['auroc']:.4f}")
logger.info(f"  AUPRC: {metrics_lr['auprc']:.4f}")
logger.info(f"  Brier: {metrics_lr['brier']:.4f}")
logger.info(f"  Accuracy: {metrics_lr['accuracy']:.4f}")
logger.info(f"  F1: {metrics_lr['f1']:.4f}")

# Run XGBoost
logger.info("\n3. Training XGBoost (with tuning)...")
xgboost = XGBoostModel(
    task_type="classification",
    random_state=42,
    n_trials=10,  # Reduced for demo
    cv_folds=3,
)

xgboost.fit(X_train, y_train, tune=True, class_weight="balanced")
logger.info(f"Best params: {xgboost.best_params}")

y_pred_xgb = xgboost.predict(X_test)
y_proba_xgb = xgboost.predict_proba(X_test)[:, 1]

metrics_xgb = compute_classification_metrics(y_test, y_pred_xgb, y_proba_xgb)
logger.info(f"\nXGBoost Results:")
logger.info(f"  AUROC: {metrics_xgb['auroc']:.4f}")
logger.info(f"  AUPRC: {metrics_xgb['auprc']:.4f}")
logger.info(f"  Brier: {metrics_xgb['brier']:.4f}")
logger.info(f"  Accuracy: {metrics_xgb['accuracy']:.4f}")
logger.info(f"  F1: {metrics_xgb['f1']:.4f}")

# Save results
results = {
    "dataset": "compas_two_year",
    "n_samples": len(X),
    "n_features": X.shape[1],
    "n_train": len(X_train),
    "n_test": len(X_test),
    "class_distribution": {
        "negative": int(np.bincount(y)[0]),
        "positive": int(np.bincount(y)[1]),
    },
    "models": {
        "logistic": {
            "metrics": metrics_lr,
            "best_params": logistic.best_params,
        },
        "xgboost": {
            "metrics": metrics_xgb,
            "best_params": xgboost.best_params,
        },
    },
}

output_dir = Path("experiments/results/demo")
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "compas_demo_results.json"

with open(output_file, "w") as f:
    json.dump(results, f, indent=2, default=str)

logger.info(f"\n4. Results saved to: {output_file}")

# Comparison
logger.info("\n" + "=" * 80)
logger.info("MODEL COMPARISON")
logger.info("=" * 80)
logger.info(f"{'Model':<20} {'AUROC':<10} {'AUPRC':<10} {'Brier':<10} {'F1':<10}")
logger.info("-" * 80)
logger.info(
    f"{'Logistic':<20} {metrics_lr['auroc']:<10.4f} {metrics_lr['auprc']:<10.4f} "
    f"{metrics_lr['brier']:<10.4f} {metrics_lr['f1']:<10.4f}"
)
logger.info(
    f"{'XGBoost':<20} {metrics_xgb['auroc']:<10.4f} {metrics_xgb['auprc']:<10.4f} "
    f"{metrics_xgb['brier']:<10.4f} {metrics_xgb['f1']:<10.4f}"
)
logger.info("=" * 80)

# Compute fairness metrics if sensitive features available
logger.info("\n5. Computing fairness metrics...")
try:
    df_raw = loader.load_raw()
    df_processed = loader.preprocess(df_raw)
    X_full, y_full, sensitive_full = loader.get_X_y_sensitive(df_processed)

    # Get test set indices for sensitive features
    X_full_encoded, _ = loader.prepare_for_modeling(df_processed, include_compas_score=False)

    # Align indices
    from sklearn.model_selection import train_test_split
    _, _, _, _, sensitive_train, sensitive_test = train_test_split(
        X_full_encoded, y_full, sensitive_full,
        test_size=0.2, random_state=42, stratify=y_full
    )

    from evaluation import compute_fairness_metrics

    fairness_lr = compute_fairness_metrics(
        y_test, y_pred_lr, sensitive_test, y_proba_lr
    )

    fairness_xgb = compute_fairness_metrics(
        y_test, y_pred_xgb, sensitive_test, y_proba_xgb
    )

    logger.info("\nFairness Metrics (Logistic Regression):")
    for attr in ['race', 'sex', 'age_cat']:
        if attr in fairness_lr:
            logger.info(f"  {attr}:")
            logger.info(f"    Demographic Parity Diff: {fairness_lr[attr]['demographic_parity_difference']:.4f}")
            logger.info(f"    Equalized Odds Diff: {fairness_lr[attr]['equalized_odds_difference']:.4f}")

    logger.info("\nFairness Metrics (XGBoost):")
    for attr in ['race', 'sex', 'age_cat']:
        if attr in fairness_xgb:
            logger.info(f"  {attr}:")
            logger.info(f"    Demographic Parity Diff: {fairness_xgb[attr]['demographic_parity_difference']:.4f}")
            logger.info(f"    Equalized Odds Diff: {fairness_xgb[attr]['equalized_odds_difference']:.4f}")

    results["fairness"] = {
        "logistic": fairness_lr,
        "xgboost": fairness_xgb,
    }

    # Re-save with fairness metrics
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2, default=str)

except ImportError:
    logger.warning("Fairlearn not installed, skipping fairness evaluation")
except Exception as e:
    logger.warning(f"Could not compute fairness metrics: {e}")

logger.info("\n✓ Demonstration experiment complete!")
