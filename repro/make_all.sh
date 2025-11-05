#!/bin/bash
# Reproducibility script: Run all experiments from scratch
# Estimated time: ~12 hours on GPU, ~48 hours on CPU

set -e  # Exit on error

echo "========================================="
echo "TabPFN for Criminology: Full Reproduction"
echo "========================================="
echo ""

# Set environment variables for reproducibility
export PYTHONHASHSEED=0
export RANDOM_SEED=42

# Check Python version
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

if ! python -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)"; then
    echo "ERROR: Python 3.10+ required"
    exit 1
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ] && [ -z "$CONDA_PREFIX" ]; then
    echo "WARNING: No virtual environment detected. Consider activating one."
fi

echo ""
echo "Step 1: Install dependencies"
echo "----------------------------"
pip install -r requirements.txt

echo ""
echo "Step 2: Download datasets"
echo "-------------------------"
python scripts/download_data.py --datasets compas communities_crime

echo ""
echo "Step 3: Preprocess datasets"
echo "---------------------------"
python src/data/compas_loader.py
python src/data/communities_crime_loader.py

echo ""
echo "Step 4: Run baseline experiments (COMPAS)"
echo "------------------------------------------"
python experiments/run_experiment.py \
    --dataset compas \
    --models logistic xgboost lightgbm catboost \
    --cv-folds 5 \
    --tune-trials 20 \
    --output-dir experiments/results/compas/baselines

echo ""
echo "Step 5: Run TabPFN zero-shot (COMPAS)"
echo "--------------------------------------"
python experiments/run_experiment.py \
    --dataset compas \
    --models tabpfn \
    --output-dir experiments/results/compas/tabpfn

echo ""
echo "Step 6: Run TabPFN fine-tuned (COMPAS)"
echo "---------------------------------------"
python experiments/run_experiment.py \
    --dataset compas \
    --models tabpfn_ft \
    --output-dir experiments/results/compas/tabpfn_ft

echo ""
echo "Step 7: Run LocalPFN (COMPAS)"
echo "------------------------------"
python experiments/run_experiment.py \
    --dataset compas \
    --models localpfn \
    --output-dir experiments/results/compas/localpfn

echo ""
echo "Step 8: Run experiments on Communities & Crime"
echo "-----------------------------------------------"
python experiments/run_experiment.py \
    --dataset communities_crime \
    --models all \
    --cv-folds 5 \
    --output-dir experiments/results/communities_crime

echo ""
echo "Step 9: Evaluate calibration"
echo "-----------------------------"
python src/evaluation/calibration.py \
    --results-dir experiments/results/compas \
    --output-dir paper/figs/calibration

echo ""
echo "Step 10: Evaluate fairness"
echo "--------------------------"
python src/evaluation/fairness.py \
    --results-dir experiments/results/compas \
    --output-dir paper/figs/fairness

echo ""
echo "Step 11: Generate figures and tables"
echo "-------------------------------------"
python scripts/generate_paper_artifacts.py \
    --results-dir experiments/results \
    --output-dir paper

echo ""
echo "Step 12: Save package versions"
echo "-------------------------------"
python -c "from src.utils.logging_utils import save_versions; save_versions('experiments/package_versions.json')"

echo ""
echo "========================================="
echo "REPRODUCTION COMPLETE"
echo "========================================="
echo ""
echo "Results saved to: experiments/results/"
echo "Figures saved to: paper/figs/"
echo "Tables saved to: paper/tables/"
echo ""
echo "To view results summary:"
echo "  cat experiments/results/summary.txt"
echo ""
echo "To view manuscript draft:"
echo "  cat paper/manuscript_draft.md"
echo ""
