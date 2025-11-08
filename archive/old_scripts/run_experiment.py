"""Main experiment runner for TabPFN criminology research."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import argparse
import json
import logging
from datetime import datetime
from typing import Dict, Any

import numpy as np
import pandas as pd

from data import COMPASLoader, CommunitiesCrimeLoader
from models import (
    get_baseline_models,
    TabPFNModel,
    TabPFNFinetuner,
    LocalPFN,
)
from evaluation import (
    compute_classification_metrics,
    compute_calibration_metrics,
    compute_fairness_metrics,
    plot_reliability_diagram,
    FairnessAuditor,
)
from evaluation.validation import NestedCV
from utils import set_seed, setup_logger, log_versions

logger = setup_logger()


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run TabPFN criminology experiments"
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="compas",
        choices=["compas", "communities_crime"],
        help="Dataset to use",
    )
    parser.add_argument(
        "--models",
        type=str,
        nargs="+",
        default=["all"],
        help="Models to run (logistic, xgboost, tabpfn, tabpfn_ft, localpfn, all)",
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Random seed"
    )
    parser.add_argument(
        "--cv-folds", type=int, default=5, help="Number of CV folds"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("experiments/results"),
        help="Output directory",
    )
    parser.add_argument(
        "--tune-trials",
        type=int,
        default=20,
        help="Number of hyperparameter tuning trials",
    )

    return parser.parse_args()


def load_dataset(dataset_name: str, data_dir: Path):
    """Load and prepare dataset."""
    if dataset_name == "compas":
        loader = COMPASLoader(data_dir, task="two_year")
        X, y = loader.load_and_prepare(include_compas_score=False)
        task_type = "classification"

        # Load sensitive features
        df_raw = loader.load_raw()
        df = loader.preprocess(df_raw)
        _, _, sensitive = loader.get_X_y_sensitive(df)

    elif dataset_name == "communities_crime":
        loader = CommunitiesCrimeLoader(data_dir)
        X, y = loader.load_and_prepare(include_race_features=False)
        task_type = "regression"
        sensitive = None  # Communities & Crime doesn't have individual-level sensitive features

    else:
        raise ValueError(f"Unknown dataset: {dataset_name}")

    logger.info(f"Loaded {dataset_name}: {X.shape[0]} samples, {X.shape[1]} features")

    return X, y, sensitive, task_type


def run_baselines(X_train, y_train, X_test, y_test, task_type, args):
    """Run baseline models."""
    results = {}

    baseline_models = get_baseline_models(
        task_type=task_type,
        random_state=args.seed,
        n_trials=args.tune_trials,
        cv_folds=3,  # Inner CV for tuning
    )

    for model_name, model in baseline_models.items():
        if args.models != ["all"] and model_name not in args.models:
            continue

        logger.info(f"Running {model_name}...")

        try:
            # Fit with tuning
            model.fit(X_train, y_train, tune=True, scale=(model_name == "logistic"))

            # Predict
            y_pred = model.predict(X_test)

            if task_type == "classification":
                y_proba = model.predict_proba(X_test)[:, 1]
                metrics = compute_classification_metrics(y_test, y_pred, y_proba)
            else:
                from evaluation import compute_regression_metrics

                metrics = compute_regression_metrics(y_test, y_pred)

            results[model_name] = {
                "metrics": metrics,
                "best_params": model.best_params,
            }

            logger.info(f"{model_name} completed. Score: {metrics.get('auroc', metrics.get('r2', 'N/A'))}")

        except Exception as e:
            logger.error(f"Error running {model_name}: {e}")
            results[model_name] = {"error": str(e)}

    return results


def run_tabpfn(X_train, y_train, X_test, y_test, task_type, args):
    """Run TabPFN zero-shot."""
    logger.info("Running TabPFN (zero-shot)...")

    try:
        model = TabPFNModel(task_type=task_type, random_state=args.seed)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        if task_type == "classification":
            y_proba = model.predict_proba(X_test)[:, 1]
            metrics = compute_classification_metrics(y_test, y_pred, y_proba)
        else:
            from evaluation import compute_regression_metrics

            metrics = compute_regression_metrics(y_test, y_pred)

        logger.info(f"TabPFN completed. Score: {metrics.get('auroc', metrics.get('r2', 'N/A'))}")

        return {"metrics": metrics}

    except Exception as e:
        logger.error(f"Error running TabPFN: {e}")
        return {"error": str(e)}


def run_tabpfn_finetune(X_train, y_train, X_test, y_test, task_type, args):
    """Run TabPFN with fine-tuning."""
    logger.info("Running TabPFN (fine-tuned)...")

    try:
        # Split train into train/val for fine-tuning
        from sklearn.model_selection import train_test_split

        X_train_ft, X_val_ft, y_train_ft, y_val_ft = train_test_split(
            X_train, y_train, test_size=0.2, random_state=args.seed
        )

        model = TabPFNFinetuner(
            task_type=task_type,
            learning_rate=1e-5,
            batch_size=20,
            max_epochs=30,
            early_stop_patience=5,
            random_state=args.seed,
        )

        model.fit(X_train_ft, y_train_ft, X_val_ft, y_val_ft)

        y_pred = model.predict(X_test)

        if task_type == "classification":
            y_proba = model.predict_proba(X_test)[:, 1]
            metrics = compute_classification_metrics(y_test, y_pred, y_proba)
        else:
            from evaluation import compute_regression_metrics

            metrics = compute_regression_metrics(y_test, y_pred)

        logger.info(f"TabPFN fine-tuned completed. Score: {metrics.get('auroc', metrics.get('r2', 'N/A'))}")

        return {"metrics": metrics, "training_history": model.training_history}

    except Exception as e:
        logger.error(f"Error running TabPFN fine-tuning: {e}")
        return {"error": str(e)}


def run_localpfn(X_train, y_train, X_test, y_test, task_type, args):
    """Run LocalPFN (retrieval + fine-tuning)."""
    logger.info("Running LocalPFN...")

    try:
        model = LocalPFN(
            task_type=task_type,
            retrieval_k=50,
            fine_tune=True,
            learning_rate=1e-5,
            max_epochs=20,
            random_state=args.seed,
        )

        model.fit(X_train, y_train)

        y_pred, context_size = model.predict(X_test, return_context=True)

        if task_type == "classification":
            y_proba = model.predict_proba(X_test)[:, 1]
            metrics = compute_classification_metrics(y_test, y_pred, y_proba)
        else:
            from evaluation import compute_regression_metrics

            metrics = compute_regression_metrics(y_test, y_pred)

        logger.info(f"LocalPFN completed. Score: {metrics.get('auroc', metrics.get('r2', 'N/A'))}")

        return {"metrics": metrics, "context_size": context_size}

    except Exception as e:
        logger.error(f"Error running LocalPFN: {e}")
        return {"error": str(e)}


def main():
    """Main experiment runner."""
    args = parse_args()

    # Set random seed
    set_seed(args.seed)

    # Log package versions
    log_versions(logger)

    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Load dataset
    data_dir = Path("data")
    X, y, sensitive, task_type = load_dataset(args.dataset, data_dir)

    # Convert to numpy
    X_array = X.values if isinstance(X, pd.DataFrame) else X
    y_array = y.values if isinstance(y, pd.Series) else y

    # Train/test split
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        X_array, y_array, test_size=0.2, random_state=args.seed, stratify=y_array if task_type == "classification" else None
    )

    logger.info(f"Train: {len(X_train)}, Test: {len(X_test)}")

    # Run experiments
    all_results = {}

    # Baselines
    if "all" in args.models or any(
        m in args.models for m in ["logistic", "xgboost", "lightgbm", "catboost", "random_forest"]
    ):
        baseline_results = run_baselines(
            X_train, y_train, X_test, y_test, task_type, args
        )
        all_results.update(baseline_results)

    # TabPFN
    if "all" in args.models or "tabpfn" in args.models:
        tabpfn_results = run_tabpfn(
            X_train, y_train, X_test, y_test, task_type, args
        )
        all_results["tabpfn"] = tabpfn_results

    # TabPFN fine-tuned
    if "all" in args.models or "tabpfn_ft" in args.models:
        tabpfn_ft_results = run_tabpfn_finetune(
            X_train, y_train, X_test, y_test, task_type, args
        )
        all_results["tabpfn_finetuned"] = tabpfn_ft_results

    # LocalPFN
    if "all" in args.models or "localpfn" in args.models:
        localpfn_results = run_localpfn(
            X_train, y_train, X_test, y_test, task_type, args
        )
        all_results["localpfn"] = localpfn_results

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = args.output_dir / f"{args.dataset}_{timestamp}.json"

    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2, default=str)

    logger.info(f"Results saved to {output_file}")

    # Print summary
    print("\n" + "=" * 80)
    print("EXPERIMENT SUMMARY")
    print("=" * 80)

    for model_name, result in all_results.items():
        if "error" in result:
            print(f"{model_name}: ERROR - {result['error']}")
        else:
            metrics = result.get("metrics", {})
            if task_type == "classification":
                print(
                    f"{model_name}: AUROC={metrics.get('auroc', 'N/A'):.4f}, "
                    f"AUPRC={metrics.get('auprc', 'N/A'):.4f}, "
                    f"Brier={metrics.get('brier', 'N/A'):.4f}"
                )
            else:
                print(
                    f"{model_name}: RMSE={metrics.get('rmse', 'N/A'):.4f}, "
                    f"MAE={metrics.get('mae', 'N/A'):.4f}, "
                    f"R²={metrics.get('r2', 'N/A'):.4f}"
                )

    print("=" * 80)


if __name__ == "__main__":
    main()
