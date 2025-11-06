"""
Master script to run all experiments systematically.

This script orchestrates the full experimental pipeline:
1. Runs all baseline models on COMPAS
2. Runs TabPFN variants (if available)
3. Generates fairness and calibration analyses
4. Creates all publication figures
5. Computes bootstrap confidence intervals
6. Populates manuscript with results

Usage:
    # Run everything (estimated: 2-4 hours)
    python scripts/run_all_experiments.py --full

    # Run only baselines (estimated: 30-60 minutes)
    python scripts/run_all_experiments.py --baselines-only

    # Run only TabPFN (estimated: 1-2 hours)
    python scripts/run_all_experiments.py --tabpfn-only
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import argparse
import subprocess
import time
from datetime import datetime

from utils import setup_logger

logger = setup_logger("run_all_experiments")


def run_command(cmd: list, description: str, timeout: int = None) -> bool:
    """Run a command and log output."""

    logger.info(f"\n{'='*80}")
    logger.info(f"{description}")
    logger.info(f"{'='*80}")
    logger.info(f"Command: {' '.join(cmd)}")
    logger.info(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    start_time = time.time()

    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        elapsed = time.time() - start_time

        logger.info(f"Status: SUCCESS (elapsed: {elapsed:.1f}s)")

        if result.stdout:
            logger.info(f"Output:\n{result.stdout}")

        return True

    except subprocess.CalledProcessError as e:
        elapsed = time.time() - start_time

        logger.error(f"Status: FAILED (elapsed: {elapsed:.1f}s)")
        logger.error(f"Error:\n{e.stderr}")

        return False

    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time

        logger.error(f"Status: TIMEOUT (elapsed: {elapsed:.1f}s)")

        return False


def run_baseline_experiments(dataset: str, output_dir: Path, cv_folds: int = 5, tune_trials: int = 20):
    """Run all baseline models."""

    logger.info(f"\nRunning baseline experiments on {dataset}...")

    models = ["logistic", "xgboost", "lightgbm", "catboost"]

    for model in models:
        cmd = [
            "python", "experiments/run_experiment.py",
            "--dataset", dataset,
            "--models", model,
            "--cv-folds", str(cv_folds),
            "--tune-trials", str(tune_trials),
            "--output-dir", str(output_dir / dataset / "baselines" / model),
        ]

        success = run_command(
            cmd,
            f"Running {model} on {dataset}",
            timeout=3600,  # 1 hour per model
        )

        if not success:
            logger.warning(f"Failed to run {model}, continuing with next model...")


def run_tabpfn_experiments(dataset: str, output_dir: Path):
    """Run TabPFN variants."""

    logger.info(f"\nRunning TabPFN experiments on {dataset}...")

    # Check if TabPFN is installed
    try:
        import tabpfn
        logger.info("TabPFN is installed")
    except ImportError:
        logger.warning("TabPFN is not installed. Skipping TabPFN experiments.")
        logger.info("To install TabPFN: pip install tabpfn")
        return

    tabpfn_models = ["tabpfn"]  # Add "tabpfn_ft", "localpfn" when implemented

    for model in tabpfn_models:
        cmd = [
            "python", "experiments/run_experiment.py",
            "--dataset", dataset,
            "--models", model,
            "--output-dir", str(output_dir / dataset / "tabpfn" / model),
        ]

        success = run_command(
            cmd,
            f"Running {model} on {dataset}",
            timeout=7200,  # 2 hours for TabPFN
        )

        if not success:
            logger.warning(f"Failed to run {model}, continuing...")


def run_fairness_analysis(results_dir: Path, output_dir: Path):
    """Run fairness analysis on all results."""

    cmd = [
        "python", "scripts/analyze_fairness.py",
        "--results", str(results_dir),
        "--output", str(output_dir),
    ]

    run_command(cmd, "Analyzing fairness metrics", timeout=600)


def run_calibration_analysis(results_dir: Path, output_dir: Path):
    """Run calibration analysis on all results."""

    cmd = [
        "python", "scripts/analyze_calibration.py",
        "--results", str(results_dir),
        "--output", str(output_dir),
    ]

    run_command(cmd, "Analyzing calibration metrics", timeout=600)


def generate_figures(results_dir: Path, output_dir: Path, dataset: str):
    """Generate all publication figures."""

    cmd = [
        "python", "scripts/generate_figures.py",
        "--results", str(results_dir),
        "--output", str(output_dir),
        "--dataset", dataset,
    ]

    run_command(cmd, "Generating publication figures", timeout=600)


def run_bootstrap_ci(results_dir: Path, n_bootstrap: int = 1000):
    """Compute bootstrap confidence intervals."""

    cmd = [
        "python", "scripts/run_bootstrap_ci.py",
        "--results", str(results_dir),
        "--n-bootstrap", str(n_bootstrap),
    ]

    run_command(cmd, "Computing bootstrap confidence intervals", timeout=1800)


def populate_manuscript(results_dir: Path, manuscript_path: Path):
    """Populate manuscript with results."""

    cmd = [
        "python", "scripts/populate_manuscript.py",
        "--results", str(results_dir),
        "--manuscript", str(manuscript_path),
    ]

    run_command(cmd, "Populating manuscript with results", timeout=300)


def main():
    parser = argparse.ArgumentParser(description="Run all experiments systematically")

    # Experiment selection
    parser.add_argument("--full", action="store_true",
                       help="Run complete pipeline (baselines + TabPFN + analysis)")
    parser.add_argument("--baselines-only", action="store_true",
                       help="Run only baseline models")
    parser.add_argument("--tabpfn-only", action="store_true",
                       help="Run only TabPFN variants")
    parser.add_argument("--analysis-only", action="store_true",
                       help="Run only analysis scripts (requires existing results)")

    # Configuration
    parser.add_argument("--dataset", type=str, default="compas",
                       help="Dataset to run experiments on")
    parser.add_argument("--output-dir", type=Path, default=Path("experiments/results"),
                       help="Output directory for results")
    parser.add_argument("--cv-folds", type=int, default=5,
                       help="Number of CV folds")
    parser.add_argument("--tune-trials", type=int, default=20,
                       help="Number of Optuna trials for hyperparameter tuning")
    parser.add_argument("--n-bootstrap", type=int, default=1000,
                       help="Number of bootstrap iterations")

    args = parser.parse_args()

    # Default to full pipeline if no flags specified
    if not any([args.full, args.baselines_only, args.tabpfn_only, args.analysis_only]):
        args.full = True

    logger.info("="*80)
    logger.info("COMPREHENSIVE EXPERIMENT PIPELINE")
    logger.info("="*80)
    logger.info(f"Dataset: {args.dataset}")
    logger.info(f"Output directory: {args.output_dir}")
    logger.info(f"CV folds: {args.cv_folds}")
    logger.info(f"Tuning trials: {args.tune_trials}")
    logger.info(f"Bootstrap iterations: {args.n_bootstrap}")
    logger.info(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    start_time = time.time()

    # Create output directories
    args.output_dir.mkdir(parents=True, exist_ok=True)
    figs_dir = Path("paper/figs")
    figs_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Baseline experiments
    if args.full or args.baselines_only:
        logger.info("\n" + "="*80)
        logger.info("STEP 1: BASELINE EXPERIMENTS")
        logger.info("="*80)

        run_baseline_experiments(
            args.dataset,
            args.output_dir,
            args.cv_folds,
            args.tune_trials,
        )

    # Step 2: TabPFN experiments
    if args.full or args.tabpfn_only:
        logger.info("\n" + "="*80)
        logger.info("STEP 2: TABPFN EXPERIMENTS")
        logger.info("="*80)

        run_tabpfn_experiments(args.dataset, args.output_dir)

    # Step 3: Analysis
    if args.full or args.analysis_only:
        logger.info("\n" + "="*80)
        logger.info("STEP 3: ANALYSIS")
        logger.info("="*80)

        results_dir = args.output_dir / args.dataset

        # Fairness analysis
        logger.info("\n--- Fairness Analysis ---")
        run_fairness_analysis(results_dir, figs_dir / "fairness")

        # Calibration analysis
        logger.info("\n--- Calibration Analysis ---")
        run_calibration_analysis(results_dir, figs_dir / "calibration")

        # Generate figures
        logger.info("\n--- Figure Generation ---")
        generate_figures(args.output_dir, figs_dir, args.dataset)

        # Bootstrap CIs
        logger.info("\n--- Bootstrap Confidence Intervals ---")
        run_bootstrap_ci(results_dir, args.n_bootstrap)

        # Populate manuscript
        logger.info("\n--- Manuscript Population ---")
        populate_manuscript(args.output_dir, Path("paper/manuscript_draft.md"))

    # Final summary
    elapsed = time.time() - start_time
    hours = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)
    seconds = int(elapsed % 60)

    logger.info("\n" + "="*80)
    logger.info("PIPELINE COMPLETE")
    logger.info("="*80)
    logger.info(f"Total time: {hours}h {minutes}m {seconds}s")
    logger.info(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"\nResults saved to: {args.output_dir}")
    logger.info(f"Figures saved to: {figs_dir}")
    logger.info("\nNext steps:")
    logger.info("  1. Review results: cat experiments/results/summary.txt")
    logger.info("  2. View figures: ls paper/figs/")
    logger.info("  3. Check manuscript: cat paper/manuscript_draft.md")


if __name__ == "__main__":
    main()
