# Notebooks Directory

This directory contains interactive Jupyter notebooks for all analyses in the TabPFN for Criminology research project.

## Philosophy

These notebooks prioritize:
- **Transparency:** Every analytical decision is documented with rationale
- **Exploration:** Interactive analysis with visualizations at each step
- **Reproducibility:** Notebooks can be run in sequence to reproduce all results
- **Pedagogy:** Clear explanations for readers unfamiliar with methods

## Workflow Overview

Notebooks are organized sequentially by analysis phase. Run them in order:

```
00_index.ipynb                    ← Start here (master workflow guide)
    ↓
01_data_exploration/              ← Exploratory data analysis
    ↓
02_preprocessing/                 ← Data cleaning and preparation
    ↓
03_baseline_models/               ← Traditional ML models
    ↓
04_tabpfn_experiments/            ← TabPFN variants
    ↓
05_fairness_analysis/             ← Bias and fairness evaluation
    ↓
06_calibration_analysis/          ← Calibration assessment
    ↓
07_robustness_validation/         ← Sensitivity and robustness checks
    ↓
08_statistical_inference/         ← Hypothesis testing and effect sizes
    ↓
09_reporting/                     ← Publication tables and figures
```

## Directory Structure

### `00_index.ipynb`
Master notebook providing:
- Complete workflow overview
- Links to all other notebooks
- Dependencies between notebooks
- Expected runtime for each notebook
- Instructions for customization

### `01_data_exploration/`
Exploratory data analysis and data quality assessment.

**Notebooks:**
- `01a_compas_eda.ipynb` - Comprehensive EDA for COMPAS dataset
- `01b_data_quality_assessment.ipynb` - Missing data, outliers, distributional checks
- `01c_missing_data_analysis.ipynb` - MCAR/MAR/MNAR assessment
- `01d_descriptive_statistics.ipynb` - Publication Table 1 (sample characteristics)

**Outputs:**
- Exploratory visualizations
- Data quality reports
- Descriptive statistics tables

### `02_preprocessing/`
Data cleaning, feature engineering, and train/test splitting.

**Notebooks:**
- `02a_data_cleaning.ipynb` - Filtering, validation, outlier handling
- `02b_feature_engineering.ipynb` - Feature creation and transformation
- `02c_train_test_split.ipynb` - Splitting strategy and validation
- `02d_preprocessing_validation.ipynb` - Verify data quality post-processing

**Outputs:**
- Processed datasets saved to `data/processed/`
- Processing logs and metadata
- Validation reports

### `03_baseline_models/`
Traditional machine learning baselines.

**Notebooks:**
- `03a_logistic_regression.ipynb` - Logistic regression with full diagnostics
- `03b_tree_based_models.ipynb` - XGBoost, LightGBM, CatBoost
- `03c_model_comparison.ipynb` - Statistical comparison of models
- `03d_hyperparameter_tuning.ipynb` - Tuning exploration and visualization

**Outputs:**
- Trained models saved to `results/models/`
- Predictions saved to `results/predictions/`
- Performance metrics

### `04_tabpfn_experiments/`
TabPFN foundation model experiments.

**Notebooks:**
- `04a_tabpfn_zero_shot.ipynb` - Zero-shot TabPFN evaluation
- `04b_tabpfn_finetuning.ipynb` - Fine-tuning experiments
- `04c_localpfn_retrieval.ipynb` - Retrieval-augmented learning
- `04d_tabpfn_comparison.ipynb` - Compare TabPFN variants to baselines

**Outputs:**
- TabPFN predictions
- Fine-tuning logs
- Comparative performance metrics

### `05_fairness_analysis/`
Fairness and bias evaluation across sensitive groups.

**Notebooks:**
- `05a_group_metrics.ipynb` - Performance by race, sex, age
- `05b_intersectional_fairness.ipynb` - Intersectional analysis
- `05c_fairness_interventions.ipynb` - Threshold optimization, reductions
- `05d_bias_auditing.ipynb` - Comprehensive Aequitas audit

**Outputs:**
- Fairness metrics by group
- Disparity visualizations
- Fairness audit reports

### `06_calibration_analysis/`
Calibration assessment and recalibration methods.

**Notebooks:**
- `06a_reliability_diagrams.ipynb` - Visual calibration assessment
- `06b_calibration_metrics.ipynb` - Brier, ECE, MCE computation
- `06c_recalibration_methods.ipynb` - Temperature scaling, isotonic regression
- `06d_calibration_across_groups.ipynb` - Group-specific calibration

**Outputs:**
- Reliability diagrams
- Calibration metrics
- Recalibrated predictions

### `07_robustness_validation/`
Robustness checks and sensitivity analyses.

**Notebooks:**
- `07a_temporal_validation.ipynb` - Time-based validation
- `07b_spatial_validation.ipynb` - Jurisdictional holdout
- `07c_sensitivity_analysis.ipynb` - Parameter sensitivity, specification curves
- `07d_stability_assessment.ipynb` - Stability across random seeds, folds

**Outputs:**
- Robustness metrics
- Sensitivity analysis results
- Specification curve plots

### `08_statistical_inference/`
Hypothesis testing, effect sizes, and statistical comparisons.

**Notebooks:**
- `08a_hypothesis_testing.ipynb` - McNemar's, DeLong tests for model comparison
- `08b_effect_sizes.ipynb` - Cohen's d, NNE, practical significance
- `08c_power_analysis.ipynb` - Post-hoc power, sample size considerations
- `08d_multiple_comparisons.ipynb` - Bonferroni, Holm corrections

**Outputs:**
- Statistical test results
- Effect size estimates
- Corrected p-values

### `09_reporting/`
Generate publication-quality tables and figures.

**Notebooks:**
- `09a_publication_tables.ipynb` - All manuscript tables (LaTeX, CSV, XLSX)
- `09b_publication_figures.ipynb` - All manuscript figures (high-res, styled)
- `09c_supplementary_materials.ipynb` - Appendices and supplementary content
- `09d_results_summary.ipynb` - Executive summary of findings

**Outputs:**
- Tables in `results/tables/`
- Figures in `results/figures/publication_ready/`
- Supplementary materials

## Running Notebooks

### Prerequisites

Install dependencies:
```bash
pip install -r requirements.txt
```

### Sequential Execution

Run all notebooks in order:
```bash
# Option 1: Interactive (recommended for exploration)
jupyter lab

# Option 2: Automated execution
jupyter nbconvert --execute --to notebook --inplace notebooks/**/*.ipynb

# Option 3: Run specific notebook
jupyter notebook notebooks/01_data_exploration/01a_compas_eda.ipynb
```

### Notebook Execution Order

Notebooks must be run in order due to dependencies:
1. Data exploration (01)
2. Preprocessing (02) - creates processed data
3. Modeling (03, 04) - uses processed data
4. Evaluation (05, 06, 07) - uses model predictions
5. Inference (08) - uses evaluation results
6. Reporting (09) - uses all prior results

## Notebook Structure

Every notebook follows this template:

```markdown
# Title

## Overview
- **Purpose:** What this notebook does
- **Inputs:** Required data/artifacts
- **Outputs:** What gets produced
- **Runtime:** Expected execution time

## Setup
[Imports and configuration]

## Analysis
[Step-by-step analysis with code, visualizations, interpretations]

## Results Summary
[Key findings and decisions]

## Export
[Save outputs for downstream notebooks]
```

## Best Practices

1. **Run notebooks in order** - Later notebooks depend on earlier ones
2. **Don't skip cells** - Notebooks assume linear execution
3. **Check outputs** - Verify each notebook produces expected outputs
4. **Restart kernel periodically** - Ensure no hidden state dependencies
5. **Save checkpoints** - Notebooks save intermediate results for recovery

## Customization

To adapt notebooks for your research:

1. **Modify parameters** in the "Configuration" section of each notebook
2. **Add new analyses** by copying and modifying existing cells
3. **Change datasets** by updating data loading cells
4. **Adjust visualizations** using the `src.visualization` utilities

## Outputs and Artifacts

Notebooks create various outputs:

- **Data:** Saved to `data/processed/` and `data/interim/`
- **Models:** Saved to `results/models/`
- **Predictions:** Saved to `results/predictions/`
- **Figures:** Saved to `results/figures/`
- **Tables:** Saved to `results/tables/`
- **Metrics:** Saved to `results/metrics/`

## Documentation Standards

Each notebook includes:
- Clear markdown explanations before each code block
- Inline comments for complex operations
- Visualizations for all major steps
- Decision rationale for analytical choices
- References to relevant literature
- Links to documentation and data cards

## Version Control

Notebooks are version controlled with:
- Cleared outputs (to reduce repo size)
- Execution count reset to 1
- No checkpoint files

To clear outputs before committing:
```bash
jupyter nbconvert --clear-output --inplace notebooks/**/*.ipynb
```

## Getting Help

- **General questions:** See main README.md
- **Methodological questions:** See docs/methodology/
- **Ethical considerations:** See docs/ethics/
- **Data questions:** See data cards in docs/data_cards/
- **Technical issues:** Open a GitHub issue

## Citation

If using these notebooks in your research, please cite:

```bibtex
@software{tabpfn_criminology_notebooks,
  title={TabPFN for Criminology: Interactive Analysis Notebooks},
  author={[Authors]},
  year={2024},
  url={https://github.com/[repo]/TabPFN-for-Criminology}
}
```
