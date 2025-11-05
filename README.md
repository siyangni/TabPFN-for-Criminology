# TabPFN for Criminology: Domain Adaptation and Optimization

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Publication-quality research package for optimizing TabPFN (Tabular Prior-data Fitted Networks) for criminology datasets. This project implements fine-tuning, retrieval-augmented learning (LoCalPFN), and comprehensive fairness & calibration evaluation.

## Research Questions

**RQ1:** Does domain adaptation (fine-tuning TabPFN v2 or retrieval+fine-tuning) improve predictive performance vs. strong baselines on criminology datasets?

**RQ2:** How does optimization affect **calibration** (Brier score, ECE) and **fairness** (equalized odds, demographic parity) across salient groups?

**RQ3:** Are gains stable across sites, time, and subgroups (robustness & transportability)?

## Project Structure

```
TabPFN-for-Criminology/
├── data/                      # Data storage (gitignored)
│   ├── raw/                   # Original datasets
│   ├── processed/             # Cleaned & preprocessed data
│   └── external/              # External resources
├── src/                       # Source code
│   ├── data/                  # Data loaders & preprocessing
│   ├── models/                # Model implementations
│   ├── evaluation/            # Metrics & validation
│   ├── visualization/         # Plotting utilities
│   └── utils/                 # Helper functions
├── experiments/               # Experiment configs & results
│   ├── configs/               # Hydra configuration files
│   ├── results/               # Numerical results
│   └── logs/                  # Training logs
├── paper/                     # Manuscript & figures
│   ├── figs/                  # Generated figures
│   ├── tables/                # Generated tables
│   └── sections/              # Manuscript sections
├── tests/                     # Unit tests
├── repro/                     # Reproducibility scripts
├── notebooks/                 # Exploratory notebooks
├── scripts/                   # Standalone scripts
└── docs/                      # Documentation

```

## Datasets

1. **COMPAS** (ProPublica): Recidivism prediction (two-year general & violent)
2. **UCI Communities & Crime**: Community-level violent crime rate regression
3. **NCVS** (National Crime Victimization Survey): Victimization classification/regression
4. **FBI UCR/NIBRS**: Agency-level incident prediction

All datasets include comprehensive data cards documenting provenance, ethical considerations, and limitations.

## Models

### TabPFN Variants
- **Zero-shot**: Out-of-the-box TabPFN v2 inference
- **Fine-tuned**: End-to-end supervised fine-tuning
- **LoCalPFN**: Retrieval-augmented + fine-tuning (KNN in-context learning)

### Baselines
- Logistic Regression (elastic net)
- Random Forest
- XGBoost
- LightGBM
- CatBoost

All models are tuned via nested cross-validation with Optuna.

## Evaluation Framework

### Performance Metrics
- Classification: AUROC, AUPRC, Log Loss, Brier Score
- Regression: RMSE, MAE, R²

### Calibration
- Expected Calibration Error (ECE)
- Reliability diagrams
- Temperature scaling / isotonic regression

### Fairness
- Equalized Odds (TPR/FPR parity)
- Demographic Parity
- Fairness-utility tradeoff curves (ThresholdOptimizer)
- Intersectional analysis via Aequitas

### Validation Strategies
- Nested cross-validation (stratified by group)
- Temporal validation (train past, test future)
- Jurisdictional holdout (test on unseen sites)

## Installation

### Option 1: Conda (recommended)
```bash
conda env create -f environment.yml
conda activate tabpfn-criminology
```

### Option 2: pip + virtualenv
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### GPU Setup
For optimal performance, ensure CUDA is available:
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

## Quick Start

### 1. Download & Preprocess Data
```bash
python scripts/download_data.py --datasets compas communities_crime
python src/data/preprocess.py --dataset compas --output data/processed/
```

### 2. Run Baseline Experiments
```bash
python experiments/run_baselines.py --dataset compas --models all --cv-folds 5
```

### 3. Run TabPFN Zero-Shot
```bash
python experiments/run_tabpfn.py --dataset compas --mode zero-shot
```

### 4. Fine-tune TabPFN
```bash
python experiments/run_tabpfn.py --dataset compas --mode fine-tune \
    --lr 1e-5 --batch-size 20 --max-epochs 50 --early-stop-patience 5
```

### 5. Run LoCalPFN (Retrieval + Fine-tuning)
```bash
python experiments/run_localpfn.py --dataset compas --retrieval-k 50 \
    --fine-tune --lr 1e-5
```

### 6. Evaluate Fairness & Calibration
```bash
python src/evaluation/fairness.py --results experiments/results/compas/
python src/evaluation/calibration.py --results experiments/results/compas/
```

### 7. Generate Paper Artifacts
```bash
python scripts/generate_paper_artifacts.py --all
```

## Reproducibility

### One-Command Rebuild
To reproduce all results from scratch:
```bash
bash repro/make_all.sh
```

This script:
1. Downloads raw data
2. Preprocesses & validates data
3. Runs all experiments (baselines + TabPFN variants)
4. Computes fairness & calibration metrics
5. Generates all figures & tables
6. Compiles manuscript

Estimated runtime: ~12 hours on GPU, ~48 hours on CPU (depends on dataset sizes).

### Deterministic Execution
All experiments use fixed random seeds (42) and `PYTHONHASHSEED=0`. See `src/utils/seed.py` for details.

### Package Versions
Lockfiles are provided:
- `environment.lock.yml` (conda)
- `requirements.lock.txt` (pip)

## Testing

Run unit tests:
```bash
pytest tests/ -v --cov=src --cov-report=html
```

Run specific test modules:
```bash
pytest tests/test_data_loaders.py
pytest tests/test_fairness_metrics.py
```

## Configuration

Experiments are configured via Hydra. See `experiments/configs/` for YAML files:

```yaml
# experiments/configs/compas_finetune.yaml
dataset:
  name: compas
  task: two_year_recid
  sensitive_attrs: [race, sex, age_cat]

model:
  name: tabpfn_finetune
  lr: 1e-5
  batch_size: 20
  max_epochs: 50

validation:
  strategy: nested_cv
  outer_folds: 5
  inner_folds: 3
```

Run with custom config:
```bash
python experiments/run_tabpfn.py --config-name compas_finetune
```

## Ethics & Responsible ML

### Ethical Considerations
- **COMPAS caveat**: This dataset is widely criticized for perpetuating racial bias. We use it as a benchmark with explicit caveats and fairness evaluation.
- **Sensitive inferences**: We avoid making causal or normative claims beyond predictive performance.
- **Stakeholder costs**: We report error types (false positives vs. false negatives) and their differential impacts.

### Model & Data Cards
See `docs/model_card.md` and `docs/data_cards/` for comprehensive documentation of:
- Intended use & limitations
- Performance by group
- Fairness evaluations
- Out-of-scope use cases

### Reporting Guidelines
Results are mapped to:
- **TRIPOD+AI**: Transparent Reporting of a Multivariable Prediction Model + AI
- **PROBAST+AI**: Prediction Model Risk of Bias Assessment Tool + AI

See `paper/appendix_reporting_checklist.md`.

## Results Summary

See `RESULTS.md` for headline findings, including:
- Comparative performance tables (TabPFN vs. baselines)
- Calibration & fairness metrics by group
- Robustness across temporal/jurisdictional splits
- Policy implications & limitations

## Citation

If you use this code or findings, please cite:

```bibtex
@article{tabpfn_criminology2024,
  title={Optimizing Tabular Foundation Models for Criminology:
         Fine-tuning, Retrieval, and Fairness},
  author={[Authors]},
  journal={Journal of Quantitative Criminology},
  year={2024},
  note={Under review}
}
```

## License

MIT License - see `LICENSE` file for details.

## Contributing

We welcome contributions! Please see `CONTRIBUTING.md` for guidelines.

## Contact

For questions or issues, please open a GitHub issue or contact [maintainer email].

## Acknowledgments

- **TabPFN**: [PriorLabs](https://github.com/PriorLabs/TabPFN)
- **LoCalPFN**: [Layer 6 AI](https://layer6.ai/introducing-localpfn-to-improve-tabular-foundation-models/)
- **ProPublica**: COMPAS dataset
- **UCI Machine Learning Repository**: Communities & Crime dataset
- **BJS**: NCVS API access
- **FBI**: Crime Data Explorer API
