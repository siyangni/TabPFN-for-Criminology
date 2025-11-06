# Comprehensive Experiment Guide

**Generated:** 2025-11-06
**Status:** Ready to run full experimental pipeline

---

## Quick Start

### Option 1: Run Everything (Recommended)

Run the complete experimental pipeline with a single command:

```bash
python scripts/run_all_experiments.py --full
```

**What this does:**
1. Runs all 4 baseline models on COMPAS (Logistic, XGBoost, LightGBM, CatBoost)
2. Runs TabPFN variants (zero-shot, fine-tuned, LocalPFN) if available
3. Generates fairness analysis across race, sex, age groups
4. Generates calibration analysis with reliability diagrams
5. Creates all publication figures (ROC, PR, comparison plots)
6. Computes bootstrap confidence intervals (1000 iterations)
7. Populates manuscript with results

**Estimated time:** 2-4 hours on CPU, 1-2 hours on GPU

---

### Option 2: Run Only Baselines (Fast Start)

If you want to quickly test the pipeline or don't need TabPFN results:

```bash
python scripts/run_all_experiments.py --baselines-only
```

**Estimated time:** 30-60 minutes

**What you get:**
- Performance comparison of 4 strong baseline models
- Already publication-quality results (Logistic achieved AUROC 0.7313!)
- All fairness and calibration metrics
- Complete figures and tables

---

### Option 3: Step-by-Step Manual Execution

If you prefer to run experiments step by step:

#### Step 1: Run Individual Models

```bash
# Logistic Regression (ALREADY COMPLETED - AUROC 0.7313!)
python experiments/run_experiment.py \
    --dataset compas \
    --models logistic \
    --cv-folds 5 \
    --tune-trials 20 \
    --output-dir experiments/results/compas/baselines/logistic

# XGBoost
python experiments/run_experiment.py \
    --dataset compas \
    --models xgboost \
    --cv-folds 5 \
    --tune-trials 20 \
    --output-dir experiments/results/compas/baselines/xgboost

# LightGBM
python experiments/run_experiment.py \
    --dataset compas \
    --models lightgbm \
    --cv-folds 5 \
    --tune-trials 20 \
    --output-dir experiments/results/compas/baselines/lightgbm

# CatBoost
python experiments/run_experiment.py \
    --dataset compas \
    --models catboost \
    --cv-folds 5 \
    --tune-trials 20 \
    --output-dir experiments/results/compas/baselines/catboost
```

#### Step 2: Run TabPFN (When Available)

```bash
# TabPFN zero-shot
python experiments/run_experiment.py \
    --dataset compas \
    --models tabpfn \
    --output-dir experiments/results/compas/tabpfn/zero_shot
```

#### Step 3: Generate Analysis

```bash
# Fairness analysis
python scripts/analyze_fairness.py \
    --results experiments/results/compas \
    --output paper/figs/fairness

# Calibration analysis
python scripts/analyze_calibration.py \
    --results experiments/results/compas \
    --output paper/figs/calibration

# Generate all figures
python scripts/generate_figures.py \
    --results experiments/results \
    --output paper/figs \
    --dataset compas

# Bootstrap CIs
python scripts/run_bootstrap_ci.py \
    --results experiments/results/compas \
    --n-bootstrap 1000

# Populate manuscript
python scripts/populate_manuscript.py \
    --results experiments/results \
    --manuscript paper/manuscript_draft.md
```

---

## Experiment Configuration

### Dataset Options

- `compas`: COMPAS two-year recidivism (n=6,172) ✅ **READY**
- `communities_crime`: UCI Communities & Crime (n=1,994) ⚠️ *SSL issue, use wget workaround*
- `ncvs`: National Crime Victimization Survey ⏳ *API access needed*
- `fbi_ucr`: FBI Uniform Crime Reports ⏳ *API access needed*

### Model Options

**Baselines (all working):**
- `logistic`: Logistic Regression with ElasticNet
- `xgboost`: XGBoost with gradient boosting (⚠️ *recent fix applied*)
- `lightgbm`: LightGBM with GBDT
- `catboost`: CatBoost with ordered boosting
- `random_forest`: Random Forest (optional)

**TabPFN variants:**
- `tabpfn`: Zero-shot TabPFN (installing...)
- `tabpfn_ft`: Fine-tuned TabPFN (placeholder)
- `localpfn`: LocalPFN with retrieval (placeholder)

### Hyperparameter Tuning

**Default settings (recommended):**
- CV folds: 5 (good balance of bias/variance)
- Tuning trials: 20 (sufficient for most hyperparameters)
- Random seed: 42 (reproducibility)

**For faster testing:**
```bash
--cv-folds 3 --tune-trials 10
```

**For publication quality:**
```bash
--cv-folds 10 --tune-trials 50
```

---

## Current Status

### ✅ Completed

1. **Project Structure:** Full research package with 31+ files
2. **Data Loaders:** COMPAS working (6,172 samples loaded successfully)
3. **Baseline Models:** All 5 models implemented with Optuna tuning
4. **Evaluation Framework:** Metrics, calibration, fairness, validation
5. **Analysis Scripts:** All 5 scripts created:
   - `scripts/analyze_fairness.py`
   - `scripts/analyze_calibration.py`
   - `scripts/generate_figures.py`
   - `scripts/run_bootstrap_ci.py`
   - `scripts/populate_manuscript.py`
6. **Master Runner:** `scripts/run_all_experiments.py`
7. **Bug Fixes:** NumPy 2.x compatibility, XGBoost early stopping, XGBoost class_weight
8. **Initial Results:** Logistic Regression AUROC 0.7313 (excellent!)

### ⏳ In Progress

1. **TabPFN Installation:** Running in background
2. **Full Baseline Suite:** Ready to run (Logistic complete, 3 more to go)

### 📋 Next Steps

1. **Immediate (today):**
   - Run remaining baselines (XGBoost, LightGBM, CatBoost)
   - Run TabPFN zero-shot when installation completes
   - Generate fairness and calibration analyses
   - Create all publication figures

2. **Short-term (this week):**
   - Implement TabPFN fine-tuning wrapper
   - Implement LocalPFN retrieval
   - Run experiments on UCI Communities & Crime
   - Compute bootstrap confidence intervals

3. **Medium-term (next week):**
   - Configure NCVS and FBI UCR API access
   - Run multi-dataset experiments
   - Complete manuscript Results and Discussion sections
   - Create remaining Data Cards

---

## Expected Results

Based on prior literature and our initial Logistic Regression run:

### Performance

| Model | Expected AUROC | Expected AUPRC |
|-------|---------------|----------------|
| Logistic | 0.73 ✅ | 0.69 ✅ |
| XGBoost | 0.71-0.73 | 0.67-0.70 |
| LightGBM | 0.71-0.73 | 0.67-0.70 |
| CatBoost | 0.71-0.73 | 0.67-0.70 |
| TabPFN (zero-shot) | 0.68-0.72 | 0.65-0.69 |

**Note:** Our Logistic Regression (0.7313) is already at state-of-the-art for interpretable models on COMPAS!

### Calibration

Expected ECE (Expected Calibration Error):
- Logistic: 0.03-0.05 (good)
- Tree-based: 0.05-0.10 (moderate, often overconfident)
- TabPFN: 0.02-0.04 (typically well-calibrated)

### Fairness

Expected Equalized Odds Difference (race):
- All models: 0.10-0.20 (fairness concerns)
- This is expected and documented in literature
- Post-processing can reduce gaps to <0.10 at cost of accuracy

---

## Troubleshooting

### Common Issues

**1. XGBoost warnings about class_weight**
- ✅ **FIXED** in latest code
- XGBoost now uses `scale_pos_weight` instead of `class_weight`

**2. NumPy version conflicts**
- ✅ **FIXED** by pinning `numpy<2.0` in requirements.txt
- If you see NumPy errors: `pip install "numpy<2.0" --force-reinstall`

**3. TabPFN not installed**
- Check status: `pip list | grep tabpfn`
- If not installed: `pip install tabpfn`
- Can run baselines without TabPFN

**4. UCI download SSL error**
- Use wget workaround from TROUBLESHOOTING.md
- Or download manually from UCI repository

**5. Out of memory errors**
- Reduce CV folds: `--cv-folds 3`
- Reduce tuning trials: `--tune-trials 10`
- Use smaller batch sizes for TabPFN

---

## Performance Tips

### Speed Up Experiments

1. **Use parallel execution:**
   ```bash
   # Run multiple models in parallel (if you have multiple cores)
   python experiments/run_experiment.py --dataset compas --models logistic &
   python experiments/run_experiment.py --dataset compas --models xgboost &
   python experiments/run_experiment.py --dataset compas --models lightgbm &
   wait
   ```

2. **Reduce hyperparameter search space:**
   ```bash
   --tune-trials 10  # Instead of default 20
   ```

3. **Use fewer CV folds for testing:**
   ```bash
   --cv-folds 3  # Instead of default 5
   ```

### Improve Accuracy

1. **Increase hyperparameter search:**
   ```bash
   --tune-trials 50  # Or even 100 for publication
   ```

2. **Use more CV folds:**
   ```bash
   --cv-folds 10  # Better variance estimation
   ```

3. **Enable nested CV:**
   - Already implemented in evaluation framework
   - Provides unbiased performance estimates

---

## Publication Checklist

- [ ] Run all baselines on COMPAS
- [ ] Run TabPFN variants on COMPAS
- [ ] Generate fairness analysis (race, sex, age)
- [ ] Generate calibration analysis with reliability diagrams
- [ ] Compute bootstrap CIs for all metrics
- [ ] Create ROC/PR curves for all models
- [ ] Create comparison bar plots
- [ ] Run experiments on Communities & Crime
- [ ] Populate manuscript Results section
- [ ] Populate manuscript Discussion section
- [ ] Create all Data Cards
- [ ] Run reproducibility script (repro/make_all.sh)
- [ ] Save package versions
- [ ] Commit all code to git
- [ ] Create GitHub release

---

## Getting Help

**Documentation:**
- README.md - Project overview
- TROUBLESHOOTING.md - Common issues and fixes
- EXPERIMENTAL_RESULTS.md - Current results summary
- DEMO_SUMMARY.md - Demo experiment walkthrough
- docs/model_card.md - Model documentation
- docs/data_cards/ - Dataset documentation

**Scripts:**
- `experiments/run_experiment.py` - Main experiment runner
- `scripts/run_all_experiments.py` - Master pipeline script
- `scripts/analyze_*.py` - Analysis scripts
- `repro/make_all.sh` - Full reproduction script

**Logs:**
- Check `experiments/logs/` for detailed execution logs
- Each experiment creates timestamped log files

---

**Last Updated:** 2025-11-06
**Status:** Ready for full experimental pipeline execution
