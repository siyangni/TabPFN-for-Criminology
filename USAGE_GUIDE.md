# TabPFN for Criminology: Usage Guide

**Version:** 1.0.0
**Date:** 2025-11-08
**Status:** Complete (Phases 1-4)

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Running the Analysis](#running-the-analysis)
5. [Workflow Overview](#workflow-overview)
6. [Detailed Phase Instructions](#detailed-phase-instructions)
7. [Understanding Outputs](#understanding-outputs)
8. [Customization Guide](#customization-guide)
9. [Troubleshooting](#troubleshooting)
10. [FAQ](#faq)

---

## Quick Start

**For first-time users who want to run the complete analysis:**

```bash
# 1. Clone the repository
git clone https://github.com/[username]/TabPFN-for-Criminology.git
cd TabPFN-for-Criminology

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify data is present
ls data/raw/  # Should contain COMPAS dataset

# 4. Launch Jupyter
jupyter lab notebooks/

# 5. Run notebooks sequentially
# Start with: 01_data_exploration/01a_compas_eda.ipynb
# Continue through all 22 notebooks in order
```

**Expected Total Runtime:** 4-7 hours (depending on hardware and hyperparameter tuning trials)

---

## Prerequisites

### System Requirements

**Minimum:**
- Python 3.8 or higher
- 8 GB RAM
- 10 GB disk space
- CPU-only (slower but functional)

**Recommended:**
- Python 3.9+
- 16+ GB RAM
- 20 GB disk space
- GPU with CUDA support (for faster tree model tuning)

### Knowledge Prerequisites

**For Running the Analysis:**
- Basic familiarity with Jupyter notebooks
- Understanding of Python syntax (reading, not necessarily writing)

**For Understanding the Results:**
- Criminology background (recidivism, risk assessment)
- Basic statistics (p-values, confidence intervals)
- Familiarity with classification metrics (AUROC, precision, recall)

**For Extending the Analysis:**
- Intermediate Python programming
- Machine learning fundamentals
- Statistical hypothesis testing
- Fairness in ML concepts

---

## Installation

### Option 1: Pip (Recommended for Most Users)

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import sklearn, xgboost, lightgbm, catboost; print('All dependencies installed')"
```

### Option 2: Conda (For Conda Users)

```bash
# Create conda environment
conda env create -f environment.yml
conda activate tabpfn-criminology

# Verify installation
python -c "import sklearn, xgboost, lightgbm, catboost; print('All dependencies installed')"
```

### Option 3: Minimal Installation (Notebooks Only, No TabPFN)

If you only want to explore the methodology without running TabPFN:

```bash
pip install pandas numpy scikit-learn matplotlib seaborn scipy jupyter
pip install xgboost lightgbm catboost optuna

# Skip: pip install tabpfn  (optional)
```

**Note:** You can still run all notebooks except `04_tabpfn_experiments/` without TabPFN installed.

---

## Running the Analysis

### Sequential Execution (Recommended for First Time)

The repository is designed to be run **sequentially** through 22 notebooks:

#### **Phase 2: Data Exploration & Baseline Models (12 notebooks)**

```bash
jupyter notebook notebooks/01_data_exploration/01a_compas_eda.ipynb
```

**Complete in order:**
1. `01a_compas_eda.ipynb` → Exploratory data analysis
2. `01b_data_quality_assessment.ipynb` → Outliers, VIF, normality
3. `01c_missing_data_analysis.ipynb` → Missing data patterns
4. `01d_descriptive_statistics.ipynb` → Publication-ready Table 1
5. `02a_data_cleaning.ipynb` → CONSORT-style filtering
6. `02b_feature_engineering.ipynb` → Transformations, encoding
7. `02c_train_test_split.ipynb` → Stratified split, CV folds
8. `02d_preprocessing_validation.ipynb` → Leakage checks
9. `03a_logistic_regression.ipynb` → ElasticNet baseline
10. `03b_tree_based_models.ipynb` → XGBoost, LightGBM, CatBoost
11. `03c_model_comparison.ipynb` → DeLong tests, Holm correction
12. `03d_hyperparameter_tuning.ipynb` → Comprehensive tuning analysis

**Runtime:** 2-3 hours

#### **Phase 3: TabPFN Experiments (6 notebooks)**

```bash
jupyter notebook notebooks/04_tabpfn_experiments/04a_tabpfn_zeroshot.ipynb
```

**Complete in order:**
1. `04a_tabpfn_zeroshot.ipynb` → Zero-shot evaluation
2. `04b_tabpfn_finetuned.ipynb` → Calibration (Platt scaling)
3. `04c_tabpfn_vs_baselines.ipynb` → All 6 models comparison
4. `04d_tabpfn_sensitivity.ipynb` → Robustness analysis
5. `04e_tabpfn_interpretation.ipynb` → SHAP, attention, confidence
6. `04f_tabpfn_limitations.ipynb` → **CRITICAL EVALUATION** ★

**Runtime:** 1-2 hours

#### **Phase 4: Fairness Analysis (4 notebooks)**

```bash
jupyter notebook notebooks/05_fairness_analysis/05a_group_metrics.ipynb
```

**Complete in order:**
1. `05a_group_metrics.ipynb` → 5 fairness criteria, all groups
2. `05b_fairness_constraints.ipynb` → Post-processing interventions
3. `05c_intersectionality.ipynb` → Race × Gender × Age
4. `05d_fairness_tradeoffs.ipynb` → Pareto frontiers, policy recs

**Runtime:** 1-2 hours

---

### Batch Execution (Advanced Users)

If you want to run all notebooks non-interactively (e.g., for replication):

```bash
# Install nbconvert
pip install nbconvert

# Convert all notebooks to scripts and run
for notebook in notebooks/*/*.ipynb; do
    jupyter nbconvert --to script --execute "$notebook"
done
```

**Warning:** This will take 4-7 hours and requires sufficient RAM/disk space.

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PHASE 1: FOUNDATION                              │
│  • Read: docs/methodology/analysis_plan.md                          │
│  • Read: docs/ethics/ethical_framework.md                           │
│  • Utilities available in src/statistics/                           │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│              PHASE 2: DATA & BASELINE MODELS (12 notebooks)         │
│  Start → 01a → 01b → 01c → 01d → 02a → 02b → 02c → 02d →          │
│          03a → 03b → 03c → 03d                                      │
│  Output: Cleaned data, 4 baseline models, comparison metrics        │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│            PHASE 3: TabPFN EXPERIMENTS (6 notebooks)                │
│  Start → 04a → 04b → 04c → 04d → 04e → 04f                         │
│  Output: TabPFN models, statistical comparisons, limitations        │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│             PHASE 4: FAIRNESS ANALYSIS (4 notebooks)                │
│  Start → 05a → 05b → 05c → 05d                                     │
│  Output: Fairness metrics, trade-off analysis, policy recs          │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Decision Points

**After Phase 2 (Baseline Models):**
- ✅ Continue to Phase 3 (TabPFN) if interested in transformer-based methods
- ⏭️ Skip to Phase 4 (Fairness) if only interested in traditional models

**After Phase 3 (TabPFN):**
- ✅ Continue to Phase 4 (Fairness) for complete analysis
- ⏹️ Stop here if only benchmarking TabPFN performance

**After Phase 4 (Fairness):**
- ✅ Analysis complete! Review results in `results/` directory
- 📝 Use outputs for publication, policy briefs, or teaching

---

## Detailed Phase Instructions

### Phase 1: Foundation (Pre-Work)

**No notebooks to run.** This phase consists of documentation and utilities.

**What to do:**

1. **Read the analysis plan** (30 minutes):
   ```bash
   cat docs/methodology/analysis_plan.md
   ```
   - Understand pre-registered hypotheses
   - Review statistical tests planned
   - Note sample size justification

2. **Read the ethical framework** (45 minutes):
   ```bash
   cat docs/ethics/ethical_framework.md
   ```
   - Understand high-stakes context
   - Review stakeholder considerations
   - Note deployment barriers

3. **Review statistical utilities** (15 minutes):
   ```bash
   ls src/statistics/
   cat src/statistics/hypothesis_tests.py  # DeLong, McNemar's
   cat src/statistics/effect_sizes.py      # Cohen's d, NNE
   ```

**Total Time:** ~1.5 hours of reading

---

### Phase 2: Data & Baseline Models (12 Notebooks)

#### **01_data_exploration/** (4 notebooks, ~45 minutes)

**01a_compas_eda.ipynb** (15 min)
- **Purpose:** Comprehensive exploratory data analysis
- **Key outputs:**
  - Summary statistics by demographic groups
  - Correlation matrices
  - Distribution visualizations
- **What to check:** Are there class imbalances? Missing data patterns?

**01b_data_quality_assessment.ipynb** (15 min)
- **Purpose:** Outlier detection, multicollinearity (VIF), normality tests
- **Key outputs:**
  - Outlier identification (IQR, Z-score)
  - VIF scores for continuous features
  - Normality test results
- **What to check:** Are any features highly collinear (VIF > 10)?

**01c_missing_data_analysis.ipynb** (10 min)
- **Purpose:** Systematic missing data analysis
- **Key outputs:**
  - Missingness patterns (MCAR, MAR, MNAR)
  - Visualization of missing data
- **What to check:** Is data missing at random or systematically?

**01d_descriptive_statistics.ipynb** (5 min)
- **Purpose:** Generate publication-ready Table 1
- **Key outputs:**
  - `results/tables/table1_descriptive_statistics.csv`
  - Stratified by recidivism outcome
- **What to check:** Do groups differ on key covariates?

---

#### **02_preprocessing/** (4 notebooks, ~30 minutes)

**02a_data_cleaning.ipynb** (10 min)
- **Purpose:** CONSORT-style participant flow filtering
- **Key outputs:**
  - `data/processed/compas_cleaned.parquet`
  - Exclusion flowchart data
- **What to check:** How many cases excluded? Why?

**02b_feature_engineering.ipynb** (10 min)
- **Purpose:** Log transforms, standardization, encoding
- **Key outputs:**
  - `data/processed/compas_engineered.parquet`
  - Feature transformation log
- **What to check:** Are transformations appropriate for distributions?

**02c_train_test_split.ipynb** (5 min)
- **Purpose:** Stratified 80/20 split + 5-fold CV indices
- **Key outputs:**
  - `data/processed/X_train.parquet`, `X_test.parquet`
  - `data/processed/y_train.parquet`, `y_test.parquet`
  - `data/processed/cv_folds.json`
- **What to check:** Are train/test splits balanced?

**02d_preprocessing_validation.ipynb** (5 min)
- **Purpose:** Check for data leakage, validate transformations
- **Key outputs:**
  - Validation report
- **What to check:** Any leakage detected? Transformations reversible?

---

#### **03_baseline_models/** (4 notebooks, ~1 hour)

**03a_logistic_regression.ipynb** (15 min)
- **Purpose:** ElasticNet logistic regression with Optuna tuning
- **Key outputs:**
  - `results/models/logistic_regression_tuned.pkl`
  - `results/predictions/logistic_regression_predictions.parquet`
  - `results/metrics/logistic_regression_metrics.json`
- **Key metrics:** AUROC, AUPRC, Brier score, calibration
- **What to check:** Is model well-calibrated? Feature coefficients make sense?

**03b_tree_based_models.ipynb** (30 min)
- **Purpose:** XGBoost, LightGBM, CatBoost with 30 Optuna trials each
- **Key outputs:**
  - 3 trained models (`.pkl` files)
  - 3 prediction files (`.parquet`)
  - 3 metrics files (`.json`)
- **What to check:** Which tree model performs best? Overfitting concerns?
- **Note:** This is the longest notebook in Phase 2 (90 tuning trials total)

**03c_model_comparison.ipynb** (10 min)
- **Purpose:** Statistical comparison of all 4 baseline models
- **Key outputs:**
  - `results/tables/baseline_model_comparison.csv`
  - ROC curves for all models
  - DeLong test results (6 pairwise comparisons)
- **Key analysis:** Holm correction for multiple comparisons
- **What to check:** Are performance differences statistically significant?

**03d_hyperparameter_tuning.ipynb** (5 min)
- **Purpose:** Analyze hyperparameter tuning process
- **Key outputs:**
  - Tuning history visualizations
  - Parameter importance plots
- **What to check:** Did tuning converge? Any patterns in best parameters?

---

### Phase 3: TabPFN Experiments (6 Notebooks)

**Prerequisites:** Phase 2 complete (needs baseline models for comparison)

**04a_tabpfn_zeroshot.ipynb** (15 min)
- **Purpose:** Evaluate pre-trained TabPFN without fine-tuning
- **Key outputs:**
  - `results/predictions/tabpfn_zeroshot_predictions.parquet`
  - `results/metrics/tabpfn_zeroshot_metrics.json`
- **What to check:** How does zero-shot TabPFN compare to tuned baselines?

**04b_tabpfn_finetuned.ipynb** (20 min)
- **Purpose:** Apply Platt scaling calibration to TabPFN
- **Key outputs:**
  - `results/models/tabpfn_finetuned.pkl`
  - Calibration comparison plots
- **Key analysis:** DeLong test (zero-shot vs fine-tuned)
- **What to check:** Does calibration improve Brier score?

**04c_tabpfn_vs_baselines.ipynb** (20 min)
- **Purpose:** Comprehensive comparison of all 6 models
- **Key outputs:**
  - `results/tables/comprehensive_model_comparison.csv`
  - All-models ROC curve
  - Holm-corrected DeLong tests (15 comparisons)
- **Key analysis:** Multiple comparison correction
- **What to check:** Does TabPFN significantly outperform baselines?

**04d_tabpfn_sensitivity.ipynb** (15 min)
- **Purpose:** Test robustness to sample size and feature noise
- **Key outputs:**
  - Sample size sensitivity curve
  - Noise robustness results
- **What to check:** At what sample size does performance stabilize?

**04e_tabpfn_interpretation.ipynb** (20 min)
- **Purpose:** SHAP analysis, confidence distributions
- **Key outputs:**
  - SHAP summary plots
  - Confidence distribution visualizations
- **What to check:** Which features most influence predictions?
- **Note:** SHAP computation is slow (5-10 minutes)

**04f_tabpfn_limitations.ipynb** (10 min)
- **Purpose:** **CRITICAL EVALUATION** of TabPFN for criminal justice
- **Key sections:**
  - Technical limitations
  - Ethical implications
  - Deployment barriers
- **Key takeaway:** TabPFN is research tool only, NOT ready for deployment
- **What to check:** Do you agree with the limitations identified?

---

### Phase 4: Fairness Analysis (4 Notebooks)

**Prerequisites:** Phase 2 and/or Phase 3 complete (needs model predictions)

**05a_group_metrics.ipynb** (30 min)
- **Purpose:** Compute 5 fairness criteria for all demographic groups
- **Key outputs:**
  - `results/fairness/group_fairness_metrics.csv`
  - Fairness metric visualizations by group
- **5 Criteria:**
  1. Demographic Parity
  2. Equalized Odds
  3. Equal Opportunity
  4. Predictive Parity
  5. Calibration
- **What to check:** Which fairness criteria are violated? By how much?

**05b_fairness_constraints.ipynb** (20 min)
- **Purpose:** Apply post-processing fairness interventions
- **Key outputs:**
  - Threshold-adjusted predictions
  - Fairness improvement analysis
- **Key analysis:** Accuracy-fairness trade-offs
- **What to check:** How much accuracy is sacrificed for fairness gains?

**05c_intersectionality.ipynb** (30 min)
- **Purpose:** Race × Gender × Age intersectional analysis
- **Key outputs:**
  - `results/fairness/intersectional_metrics.csv`
  - Heatmaps of intersectional disparities
- **Key framework:** Crenshaw (1989) intersectionality theory
- **What to check:** Do compound disadvantages emerge at intersections?

**05d_fairness_tradeoffs.ipynb** (20 min)
- **Purpose:** Pareto frontier analysis of accuracy-fairness trade-offs
- **Key outputs:**
  - `results/fairness/pareto_frontiers.csv`
  - Pareto frontier visualizations
  - Policy recommendations
- **Key framework:** Kleinberg et al. (2017) impossibility theorems
- **What to check:** What trade-offs would different stakeholders accept?

---

## Understanding Outputs

### Directory Structure

```
results/
├── models/                 # Trained model files (.pkl, .joblib)
│   ├── logistic_regression_tuned.pkl
│   ├── xgboost_tuned.pkl
│   ├── lightgbm_tuned.pkl
│   ├── catboost_tuned.pkl
│   ├── tabpfn_zeroshot.pkl
│   └── tabpfn_finetuned.pkl
│
├── predictions/            # Model predictions (Parquet format)
│   ├── logistic_regression_predictions.parquet
│   ├── [other models]_predictions.parquet
│   └── # Columns: id, y_true, y_pred, y_proba
│
├── metrics/               # Performance metrics (JSON, CSV)
│   ├── logistic_regression_metrics.json
│   ├── baseline_model_comparison.csv
│   └── comprehensive_model_comparison.csv
│
├── fairness/              # Fairness analysis results
│   ├── group_fairness_metrics.csv
│   ├── intersectional_metrics.csv
│   └── pareto_frontiers.csv
│
├── tables/                # Publication-ready tables (CSV, LaTeX)
│   ├── table1_descriptive_statistics.csv
│   ├── baseline_model_comparison.csv
│   └── comprehensive_model_comparison.csv
│
└── figures/               # High-resolution visualizations (300 DPI)
    ├── eda/               # Exploratory data analysis plots
    ├── baselines/         # Baseline model comparisons
    ├── tabpfn/            # TabPFN-specific visualizations
    └── fairness/          # Fairness analysis plots
```

### Key Files to Review

**After Phase 2:**
- `results/tables/baseline_model_comparison.csv` - Which baseline performs best?
- `results/figures/baselines/all_models_roc.png` - Visual comparison

**After Phase 3:**
- `results/tables/comprehensive_model_comparison.csv` - TabPFN vs baselines
- `notebooks/04_tabpfn_experiments/04f_tabpfn_limitations.ipynb` - **READ THIS**

**After Phase 4:**
- `results/fairness/group_fairness_metrics.csv` - Fairness disparities
- `results/fairness/pareto_frontiers.csv` - Trade-off options
- `notebooks/05_fairness_analysis/05d_fairness_tradeoffs.ipynb` - Policy recs

---

## Customization Guide

### Using Your Own Dataset

**Requirements:**
- Binary classification problem
- Tabular data (not images/text)
- Sensitive attributes for fairness analysis (e.g., race, gender, age)
- Sample size: >1,000 (for stable estimates)

**Steps:**

1. **Prepare data in COMPAS format:**
   ```python
   # Your dataset should have:
   # - Features (X): numeric or categorical
   # - Target (y): binary (0/1)
   # - Sensitive attributes: race, sex, age_cat (or equivalents)

   import pandas as pd
   your_data = pd.read_csv('your_dataset.csv')
   your_data.to_parquet('data/raw/your_dataset.parquet')
   ```

2. **Modify notebooks:**
   - In `01a_compas_eda.ipynb`, change data loading path
   - Update feature names throughout notebooks
   - Adjust sensitive attribute names in Phase 4

3. **Re-run all notebooks sequentially**

### Adding New Models

**To add a new classifier (e.g., Random Forest):**

1. **Create new notebook:** `notebooks/03_baseline_models/03e_random_forest.ipynb`

2. **Follow template from 03a:**
   ```python
   from sklearn.ensemble import RandomForestClassifier

   def objective(trial):
       n_estimators = trial.suggest_int('n_estimators', 50, 500)
       max_depth = trial.suggest_int('max_depth', 3, 20)
       # ... more hyperparameters

       model = RandomForestClassifier(
           n_estimators=n_estimators,
           max_depth=max_depth,
           random_state=42
       )
       # ... rest of Optuna objective
   ```

3. **Add to comparison notebooks:**
   - Update `03c_model_comparison.ipynb` to include RF
   - Update `04c_tabpfn_vs_baselines.ipynb` if comparing with TabPFN

### Modifying Hyperparameter Tuning

**To change number of Optuna trials:**

In any model notebook (e.g., `03b_tree_based_models.ipynb`):

```python
# Change from:
study.optimize(objective, n_trials=30)

# To (for faster testing):
study.optimize(objective, n_trials=10)

# Or (for more thorough tuning):
study.optimize(objective, n_trials=100)
```

**Trade-off:** More trials = better hyperparameters but longer runtime.

### Adjusting Fairness Criteria

**To add a new fairness metric:**

In `notebooks/05_fairness_analysis/05a_group_metrics.ipynb`:

```python
def compute_fairness_metrics(y_true, y_pred, y_proba, group_name, group_value, n_samples):
    # ... existing metrics ...

    # Add your custom metric
    from sklearn.metrics import balanced_accuracy_score
    balanced_acc = balanced_accuracy_score(y_true, y_pred)

    return {
        # ... existing metrics ...
        'balanced_accuracy': balanced_acc,
    }
```

---

## Troubleshooting

### Common Issues

#### **Issue 1: "TabPFN not installed"**

**Error:**
```
ModuleNotFoundError: No module named 'tabpfn'
```

**Solution:**
```bash
pip install tabpfn
```

**Alternative:** Skip Phase 3 notebooks (TabPFN experiments) if not interested.

---

#### **Issue 2: "Out of memory" during hyperparameter tuning**

**Error:**
```
MemoryError: Unable to allocate array
```

**Solutions:**

1. Reduce Optuna trials:
   ```python
   study.optimize(objective, n_trials=10)  # Instead of 30
   ```

2. Reduce tree model complexity:
   ```python
   max_depth = trial.suggest_int('max_depth', 3, 10)  # Instead of 3-20
   ```

3. Use smaller CV folds:
   ```python
   cv = StratifiedKFold(n_splits=3)  # Instead of 5
   ```

---

#### **Issue 3: "Jupyter kernel dies" during SHAP computation**

**Error:**
```
The kernel appears to have died. It will restart automatically.
```

**Cause:** SHAP computation (in `04e_tabpfn_interpretation.ipynb`) is memory-intensive.

**Solutions:**

1. Reduce sample size for SHAP:
   ```python
   # In 04e_tabpfn_interpretation.ipynb
   X_sample = X_test.sample(n=100, random_state=42)  # Instead of 500
   ```

2. Use fewer background samples:
   ```python
   background = shap.sample(X_train, 50)  # Instead of 100
   ```

3. Skip SHAP section (interpretation still possible via confidence analysis)

---

#### **Issue 4: "No such file or directory: data/processed/..."**

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'data/processed/X_train.parquet'
```

**Cause:** You skipped a preprocessing notebook.

**Solution:** Run notebooks in strict sequential order:
- If missing `X_train.parquet`, run `02c_train_test_split.ipynb`
- If missing `compas_engineered.parquet`, run `02b_feature_engineering.ipynb`
- etc.

---

#### **Issue 5: "DeLong test fails with ValueError"**

**Error:**
```
ValueError: Input contains NaN or infinity
```

**Cause:** Model produced invalid predictions (NaN or inf).

**Solution:**

1. Check for data issues in preprocessing
2. Verify model convergence:
   ```python
   print(model.n_iter_)  # For logistic regression
   ```
3. Increase max_iter if not converged:
   ```python
   LogisticRegression(max_iter=2000)  # Instead of 1000
   ```

---

#### **Issue 6: "Fairness analysis shows all NaN"**

**Cause:** Sensitive attribute not found in data or all one value in group.

**Solution:**

1. Verify sensitive attribute exists:
   ```python
   print(df['race'].value_counts())
   ```

2. Check for sufficient samples per group (need n ≥ 30):
   ```python
   df.groupby(['race', 'sex', 'age_cat']).size()
   ```

3. Skip intersectional groups with n < 30

---

### Getting Help

**Before opening an issue:**

1. ✅ Check this USAGE_GUIDE.md
2. ✅ Review relevant phase summary (PHASE[1-4]_COMPLETE.md)
3. ✅ Search existing GitHub issues
4. ✅ Try running notebooks sequentially from scratch

**When opening an issue, include:**
- Which notebook you're running
- Full error message (with traceback)
- Python version (`python --version`)
- Package versions (`pip list | grep -E "(sklearn|xgboost|tabpfn)"`)
- System info (OS, RAM)

---

## FAQ

### General Questions

**Q: How long does the complete analysis take?**
A: 4-7 hours total. Phase 2 (2-3 hours), Phase 3 (1-2 hours), Phase 4 (1-2 hours).

**Q: Can I run this on a laptop?**
A: Yes, but expect longer runtimes. Minimum 8 GB RAM recommended.

**Q: Do I need a GPU?**
A: No, but hyperparameter tuning will be faster with GPU (especially for XGBoost).

**Q: Can I skip certain phases?**
A:
- Phase 2 is **required** (data preprocessing and baselines)
- Phase 3 (TabPFN) is optional if not interested
- Phase 4 (fairness) is optional but **highly recommended** for criminology research

---

### Methodological Questions

**Q: Why use DeLong test instead of simple AUROC difference?**
A: DeLong accounts for correlation between models (trained on same data). Simple comparison inflates Type I error.

**Q: Why Holm correction instead of Bonferroni?**
A: Holm is uniformly more powerful (rejects more true positives) while still controlling FWER. No reason to use Bonferroni.

**Q: What if I want to use Benjamini-Hochberg (FDR control) instead?**
A: Modify `src/statistics/multiple_comparisons.py` or apply in notebooks:
```python
from src.statistics.multiple_comparisons import benjamini_hochberg
reject, p_adjusted = benjamini_hochberg(p_values, alpha=0.05)
```

**Q: Why not use AIC/BIC for model selection?**
A: AIC/BIC are for nested models. We compare non-nested models (LR vs XGBoost vs TabPFN), so we use DeLong test.

---

### Fairness Questions

**Q: Why can't we satisfy all fairness criteria simultaneously?**
A: Kleinberg et al. (2017) impossibility theorem: When base rates differ across groups, cannot achieve demographic parity + equalized odds + predictive parity. Must make normative choice.

**Q: Which fairness criterion should I use?**
A: This is a **normative (value-based) question**, not a technical one. See `05d_fairness_tradeoffs.ipynb` for stakeholder-centered decision framework.

**Q: What if my dataset doesn't have race/gender?**
A:
- Fairness analysis requires sensitive attributes
- If not available, skip Phase 4 or use proxy variables (with caveats)
- Document limitations clearly

**Q: How do I handle intersectionality with n < 30?**
A:
- Report metrics but flag as "insufficient sample size"
- Aggregate to larger groups (e.g., "Black women" instead of "Black women age 25-45")
- Note limitation in discussion

---

### TabPFN Questions

**Q: Why does TabPFN only take a few seconds to train?**
A: It's a pre-trained transformer with in-context learning (no gradient updates). Similar to GPT-like models for tabular data.

**Q: Should I deploy TabPFN in criminal justice?**
A: **NO.** See `04f_tabpfn_limitations.ipynb` for detailed reasoning. Black-box nature incompatible with high-stakes decisions.

**Q: Can I use TabPFN for datasets >10K samples?**
A: No, hard constraint in current version. Use traditional models instead.

**Q: What if I have >100 features?**
A: TabPFN won't work. Use dimensionality reduction (PCA, feature selection) or traditional models.

---

### Publication Questions

**Q: Is this repository publication-ready?**
A: Yes, suitable for:
- Criminology research methods journals (Journal of Quantitative Criminology, Justice Quarterly)
- ML fairness conferences (FAccT, AIES)
- Policy reports (pre-trial risk assessment evaluation)

**Q: What reporting standards does this follow?**
A: TRIPOD+AI (Transparent Reporting of Multivariable Prediction Model + AI)

**Q: Can I use the figures/tables directly?**
A: Yes, all outputs are publication-ready:
- Figures: 300 DPI PNG
- Tables: CSV (for Word) and LaTeX (for manuscript)

**Q: How do I cite this repository?**
A: See citation in README.md (BibTeX format provided)

---

### Extension Questions

**Q: Can I add new models?**
A: Yes, follow template in `03a_logistic_regression.ipynb`. Add Optuna objective, train, evaluate, save predictions.

**Q: Can I use this for other datasets (not COMPAS)?**
A: Yes, see "Customization Guide" → "Using Your Own Dataset" above.

**Q: Can I implement Phases 5-8 (calibration, robustness, inference, reporting)?**
A: Yes! See `archive/old_documentation/WORKPLAN_RESTRUCTURING.md` for planned notebooks. Phases 1-4 provide foundation.

**Q: Can I contribute to this repository?**
A: Yes, contributions welcome. Follow existing code style, include tests, update documentation.

---

## Additional Resources

### Documentation

- **README.md** - Main repository overview
- **REPOSITORY_OVERVIEW.md** - Comprehensive executive summary
- **PHASE[1-4]_COMPLETE.md** - Detailed phase summaries
- **docs/methodology/analysis_plan.md** - Pre-registered analysis plan
- **docs/ethics/ethical_framework.md** - Ethical framework

### External References

**Statistical Methods:**
- DeLong test: DeLong et al. (1988), *Biometrics*
- Multiple comparisons: Holm (1979), *Scandinavian Journal of Statistics*
- Effect sizes: Cohen (1988), *Statistical Power Analysis*

**Fairness Framework:**
- Impossibility theorems: Kleinberg et al. (2017), *ITCS*
- Intersectionality: Crenshaw (1989), *University of Chicago Legal Forum*
- Fairness metrics: Verma & Rubin (2018), *IEEE*

**TabPFN:**
- Hollmann et al. (2023), *ICLR* - TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second

**COMPAS Analysis:**
- Angwin et al. (2016), *ProPublica* - Machine Bias
- Dressel & Farid (2018), *Science Advances* - The accuracy, fairness, and limits of predicting recidivism

---

## Contact & Support

**Issues:** [GitHub Issues](https://github.com/[username]/TabPFN-for-Criminology/issues)
**Email:** [your.email@institution.edu]
**Website:** [Your research website]

---

## Version History

**v1.0.0** (2025-11-08)
- Initial release with 22 notebooks (Phases 1-4 complete)
- Comprehensive documentation
- Publication-ready outputs

---

**Happy Analyzing! Remember: This is research, not a deployment system. Always prioritize transparency, fairness, and ethical considerations in criminal justice ML.**
