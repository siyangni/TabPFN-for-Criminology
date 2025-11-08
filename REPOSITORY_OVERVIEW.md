# Repository Overview: TabPFN for Criminology

**Version:** 1.0.0  
**Date:** 2025-11-08  
**Status:** Phases 1-4 Complete  
**Purpose:** Methodologically rigorous framework for evaluating ML in criminal justice

---

## Executive Summary

This repository provides a **complete, publication-ready framework** for evaluating machine learning models in criminology research. It transforms an automated script-based ML pipeline into an interactive, transparent, and ethically grounded analysis workflow with 22 comprehensive Jupyter notebooks.

### Key Contributions

1. **Methodological Rigor**: Pre-registered hypotheses, statistical tests with multiple comparison corrections, effect sizes
2. **Ethical Framework**: Comprehensive ethical considerations for high-stakes criminal justice applications
3. **Fairness Analysis**: Multi-criteria evaluation with impossibility theorems, intersectionality, trade-off analysis
4. **Critical Evaluation**: Balanced assessment of TabPFN (not advocacy) with deployment barriers clearly identified
5. **Transparency**: All decisions documented, all trade-offs explicit, stakeholder-centered recommendations

---

## Repository Contents

### Documentation (2,000+ lines)

**Foundation Documents:**
- `README.md`: Main repository documentation (430 lines)
- `WORKPLAN_RESTRUCTURING.md`: Complete transformation plan (720 lines)
- `docs/methodology/analysis_plan.md`: Pre-registered analysis plan (500 lines)
- `docs/ethics/ethical_framework.md`: Ethical framework for ML in criminal justice (800 lines)

**Phase Summaries:**
- `PHASE1_COMPLETE.md`: Foundation phase (infrastructure, statistics, ethics)
- `PHASE2_COMPLETE.md`: Core analysis (12 notebooks - data to baselines)
- `PHASE3_COMPLETE.md`: TabPFN experiments (6 notebooks - evaluation to limitations)
- `PHASE4_COMPLETE.md`: Fairness analysis (4 notebooks - groups to trade-offs)

### Code (7,100+ lines existing + 6,000+ new)

**Notebooks (22 total, ~6,000 lines):**
- Phase 2: 12 notebooks (data exploration, preprocessing, baseline models)
- Phase 3: 6 notebooks (TabPFN zero-shot, fine-tuned, comparison, sensitivity, interpretation, limitations)
- Phase 4: 4 notebooks (group metrics, fairness constraints, intersectionality, trade-offs)

**Utilities (src/):**
- `data_loader/`: Data loading and validation
- `statistics/`: Hypothesis tests, effect sizes, multiple comparison corrections

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PHASE 1: FOUNDATION                              │
│  • Statistical utilities (DeLong, McNemar's, effect sizes)          │
│  • Ethical framework (800 lines)                                    │
│  • Analysis plan (pre-registration, 500 lines)                      │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│              PHASE 2: DATA & BASELINE MODELS (12 notebooks)         │
│                                                                     │
│  01_data_exploration/ (4 notebooks)                                │
│    ├── 01a_compas_eda.ipynb            Comprehensive EDA           │
│    ├── 01b_data_quality_assessment     Outliers, VIF, normality    │
│    ├── 01c_missing_data_analysis       Missing data framework      │
│    └── 01d_descriptive_statistics      Publication-ready Table 1   │
│                                                                     │
│  02_preprocessing/ (4 notebooks)                                   │
│    ├── 02a_data_cleaning               CONSORT-style filtering     │
│    ├── 02b_feature_engineering         Transforms, encoding        │
│    ├── 02c_train_test_split            Stratified 80/20, 5-fold CV│
│    └── 02d_preprocessing_validation    Leakage checks, validation  │
│                                                                     │
│  03_baseline_models/ (4 notebooks)                                 │
│    ├── 03a_logistic_regression         ElasticNet with Optuna      │
│    ├── 03b_tree_based_models           XGBoost, LightGBM, CatBoost │
│    ├── 03c_model_comparison            DeLong tests, Holm correction│
│    └── 03d_hyperparameter_tuning       Comprehensive tuning analysis│
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│            PHASE 3: TabPFN EXPERIMENTS (6 notebooks)                │
│                                                                     │
│  04_tabpfn_experiments/                                            │
│    ├── 04a_tabpfn_zeroshot             Pre-trained, no fine-tuning │
│    ├── 04b_tabpfn_finetuned            Calibration (Platt scaling) │
│    ├── 04c_tabpfn_vs_baselines         All 6 models, 15 comparisons│
│    ├── 04d_tabpfn_sensitivity          Robustness to data variations│
│    ├── 04e_tabpfn_interpretation       SHAP, attention, confidence │
│    └── 04f_tabpfn_limitations          CRITICAL EVALUATION ★        │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│             PHASE 4: FAIRNESS ANALYSIS (4 notebooks)                │
│                                                                     │
│  05_fairness_analysis/                                             │
│    ├── 05a_group_metrics               5 fairness criteria, all groups│
│    ├── 05b_fairness_constraints        Post-processing interventions│
│    ├── 05c_intersectionality           Race × Gender × Age          │
│    └── 05d_fairness_tradeoffs          Pareto frontiers, policy recs│
└─────────────────────────────────────────────────────────────────────┘
```

---

## Key Results Structure

### Models Evaluated (6 total)

1. **Logistic Regression** - Tuned ElasticNet baseline
2. **XGBoost** - Gradient boosting (30 Optuna trials)
3. **LightGBM** - Fast gradient boosting (30 trials)
4. **CatBoost** - Categorical boosting (30 trials)
5. **TabPFN Zero-Shot** - Pre-trained transformer (no tuning)
6. **TabPFN Fine-Tuned** - Calibrated with Platt scaling

### Statistical Framework

**Hypothesis Testing:**
- DeLong test (15 pairwise AUROC comparisons)
- McNemar's test (prediction agreement)
- Permutation tests (non-parametric)

**Multiple Comparisons:**
- Holm step-down (FWER control)
- Benjamini-Hochberg (FDR control)

**Effect Sizes:**
- Cohen's d (standardized differences)
- NNE (number needed to evaluate)
- Cramér's V (categorical associations)

### Fairness Framework

**5 Criteria Evaluated:**
1. Demographic Parity
2. Equalized Odds  
3. Equal Opportunity
4. Predictive Parity
5. Calibration

**Theoretical Grounding:**
- Kleinberg et al. (2017): Impossibility theorems
- Crenshaw (1989): Intersectionality
- Stakeholder-centered trade-off decisions

**Intersectional Analysis:**
- Race × Gender
- Race × Age
- Race × Gender × Age (where n ≥ 30)

---

## Critical Insights

### 1. Impossibility Theorems

**Finding**: Cannot simultaneously satisfy all fairness criteria when base rates differ across groups.

**Implication**: Must choose which criterion to prioritize based on normative (value-based) considerations, not technical optimization.

**Action**: Stakeholder engagement essential; document choice transparently.

### 2. TabPFN Limitations

**Strengths**:
- Extremely fast (seconds vs minutes)
- No hyperparameter tuning needed
- Competitive performance

**Critical Limitations** (deployment barriers):
- Black-box (limited interpretability)
- Dataset constraints (<10K samples, <100 features)
- Accountability unclear
- Pre-trained on synthetic data (domain shift)
- **NOT ready for criminal justice deployment**

**Verdict**: Promising research tool; **NOT recommended for deployment**.

### 3. Intersectionality Matters

**Finding**: Compound disadvantages at intersections (e.g., Black women face different biases than Black men or white women).

**Implication**: Single-attribute fairness analysis insufficient.

**Action**: Always evaluate fairness at intersections; engage intersectional stakeholders.

### 4. Trade-Offs Are Normative

**Finding**: All models exhibit accuracy-fairness trade-offs; no model dominates.

**Implication**: Trade-off choice reflects values, not just technical performance.

**Action**: Report full Pareto frontier; let stakeholders choose based on priorities.

### 5. Transparency Is Essential

**Finding**: Criminal justice ML has high stakes (liberty deprivation).

**Implication**: Must document all decisions, report all metrics, acknowledge all limitations.

**Action**: Follow framework in this repository; prioritize stakeholder trust.

---

## Publication Readiness

### Suitable For

✅ **Criminology Research Methods Journals**
- Journal of Quantitative Criminology
- Justice Quarterly
- Criminology
- Crime and Delinquency

✅ **ML Fairness Conferences**
- FAccT (Fairness, Accountability, and Transparency)
- AIES (AI, Ethics, and Society)
- NeurIPS (Datasets and Benchmarks track)

✅ **Criminal Justice Policy Reports**
- Pre-trial risk assessment evaluation
- Methodology guidelines for jurisdictions
- Stakeholder engagement frameworks

### Reporting Standards Met

✅ **TRIPOD+AI**: Transparent Reporting of Multivariable Prediction Model + AI
✅ **Statistical rigor**: Pre-registration, corrections, effect sizes
✅ **Ethical framework**: High-stakes considerations documented
✅ **Fairness evaluation**: Multi-criteria with impossibility theorems
✅ **Transparency**: All decisions and trade-offs documented

---

## How to Use This Repository

### For Researchers

1. **Replication**: Run notebooks sequentially (Phases 2-4)
2. **Extension**: Add new datasets, models, or fairness metrics
3. **Template**: Use as methodological framework for similar studies
4. **Publication**: Adapt documentation for your specific context

### For Students

1. **Learning**: Work through notebooks to understand ML in criminal justice
2. **Assignments**: Use as example of rigorous research workflow
3. **Projects**: Extend with additional analyses or datasets
4. **Thesis/Dissertation**: Methodological framework for empirical work

### For Policymakers

1. **Understanding**: Read Phase 4 fairness analysis for trade-off insights
2. **Decision Framework**: Use Pareto frontiers for informed decisions
3. **Stakeholder Engagement**: Adapt recommendations for your jurisdiction
4. **Auditing**: Framework for evaluating existing risk assessment tools

### For Practitioners

1. **Critical Lens**: Understand limitations of ML in criminal justice
2. **Fairness Evaluation**: Multi-criteria assessment framework
3. **Deployment Barriers**: TabPFN limitations notebook (04f) essential reading
4. **Best Practices**: Ethical framework and pre-registration approach

---

## Limitations

### What This Repository Does NOT Do

❌ **Deployment**: Not a production-ready system for criminal justice
❌ **Advocacy**: Not promoting TabPFN or any specific model
❌ **Fairness Solution**: Cannot "solve" fairness (impossibility theorems)
❌ **Normative Guidance**: Cannot decide which fairness criterion to use
❌ **Causal Claims**: Predictive models only, no causal inference

### Known Gaps

- **Single Dataset**: COMPAS only; needs validation on other datasets
- **Temporal Validation**: Not tested across time periods (concept drift)
- **Jurisdictional Validation**: Not tested across different jurisdictions
- **Stakeholder Input**: Framework for engagement, but not implemented
- **Legal Analysis**: Interpretability requirements not fully assessed

### Future Work

- Additional datasets (UCI Communities & Crime, NCVS)
- Temporal and spatial validation
- Actual stakeholder engagement (not just framework)
- Legal compliance assessment by jurisdiction
- Causal inference extensions (if appropriate data available)

---

## Dependencies

### Core Python Packages

```
pandas >= 1.3.0
numpy >= 1.21.0
scikit-learn >= 1.0.0
matplotlib >= 3.4.0
seaborn >= 0.11.0
scipy >= 1.7.0
```

### Model-Specific

```
xgboost >= 1.5.0
lightgbm >= 3.3.0
catboost >= 1.0.0
optuna >= 3.0.0
tabpfn >= 0.1.0  # Optional
```

### Utilities

```
jupyter >= 1.0.0
notebook >= 6.4.0
joblib >= 1.1.0
shap >= 0.40.0  # For interpretation
```

---

## Quick Reference

### Important Files

| File | Purpose | Lines |
|------|---------|-------|
| `README.md` | Main documentation | 430 |
| `WORKPLAN_RESTRUCTURING.md` | Transformation plan | 720 |
| `docs/methodology/analysis_plan.md` | Pre-registration | 500 |
| `docs/ethics/ethical_framework.md` | Ethical framework | 800 |
| `PHASE1_COMPLETE.md` | Foundation summary | ~600 |
| `PHASE2_COMPLETE.md` | Core analysis summary | ~400 |
| `PHASE3_COMPLETE.md` | TabPFN experiments summary | ~450 |
| `PHASE4_COMPLETE.md` | Fairness analysis summary | ~420 |

### Key Directories

| Directory | Contents | Purpose |
|-----------|----------|---------|
| `notebooks/` | 22 Jupyter notebooks | Interactive analysis |
| `src/statistics/` | Hypothesis tests, effect sizes | Statistical utilities |
| `docs/` | Methodology, ethics | Foundation documents |
| `results/` | Models, predictions, metrics | Analysis outputs |
| `data/processed/` | Clean, split data | Ready for analysis |

### Notebook Sequence

**Phase 2** (Data → Baselines): 12 notebooks, 2-3 hours
**Phase 3** (TabPFN): 6 notebooks, 1-2 hours
**Phase 4** (Fairness): 4 notebooks, 1-2 hours
**Total**: 22 notebooks, 4-7 hours

---

## Version History

**v1.0.0** (2025-11-08)
- Initial release
- 22 notebooks across 4 phases
- Complete documentation (2,000+ lines)
- Statistical utilities (hypothesis tests, effect sizes, corrections)
- Fairness framework (impossibility theorems, intersectionality, trade-offs)
- Critical TabPFN evaluation

---

## Contact & Support

**Issues**: [GitHub Issues](https://github.com/[username]/TabPFN-for-Criminology/issues)
**Documentation**: See `README.md` and phase summary files
**Questions**: Review documentation first, then open issue

---

## Final Notes

### Remember

1. **This is research**, not a deployment system
2. **Fairness cannot be "solved"** (impossibility theorems)
3. **Trade-offs are normative**, not technical decisions
4. **Stakeholder engagement** is essential, not optional
5. **Transparency** builds trust; hiding limitations erodes it

### Philosophy

Machine learning in criminal justice is a **policy question**, not just a technical problem. This repository provides:
- **Technical rigor** for credibility
- **Ethical grounding** for legitimacy
- **Transparent reporting** for accountability
- **Stakeholder frameworks** for engagement
- **Critical assessment** for informed decision-making

Use this framework to conduct research that is:
- **Methodologically sound**
- **Ethically responsible**
- **Transparent and reproducible**
- **Critical and balanced**
- **Policy-relevant and actionable**

---

**For the full repository**: See `README.md`
**For phase details**: See `PHASE[1-4]_COMPLETE.md`
**For methodology**: See `docs/methodology/`
**For ethics**: See `docs/ethics/`
**For notebooks**: See `notebooks/` (start with 01a)
