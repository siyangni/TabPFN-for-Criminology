# Analysis Plan: TabPFN for Criminology Research

**Project Title:** Optimizing Tabular Foundation Models for Criminology: Fine-tuning, Retrieval, and Fairness

**Principal Investigator:** [To be completed]

**Date Created:** 2025-11-08

**Status:** Pre-registered Analysis Plan

**Version:** 1.0

---

## 1. Executive Summary

This document serves as a pre-registered analysis plan for evaluating TabPFN (Tabular Prior-data Fitted Networks) on criminology prediction tasks. Pre-registration enhances transparency by documenting analytical decisions before observing results, reducing researcher degrees of freedom and publication bias.

**Core Objective:** Rigorously evaluate whether domain-adapted TabPFN variants improve performance, calibration, and fairness compared to well-tuned baselines on criminal justice prediction tasks.

---

## 2. Research Questions and Hypotheses

### 2.1 Primary Research Questions

**RQ1 (Performance):** Does domain adaptation (fine-tuning TabPFN v2 or retrieval+fine-tuning) improve predictive performance vs. strong baselines on criminology datasets?

**RQ2 (Calibration & Fairness):** How does optimization affect calibration (Brier score, ECE) and fairness (equalized odds, demographic parity) across salient groups (race, sex, age)?

**RQ3 (Robustness):** Are performance gains stable across sites, time periods, and subgroups (transportability & external validity)?

### 2.2 A Priori Hypotheses

#### Primary Hypotheses

**H1 (Performance):** Fine-tuned TabPFN will achieve higher AUROC than zero-shot TabPFN on COMPAS recidivism prediction.
- **Direction:** Fine-tuned > Zero-shot
- **Magnitude:** Expected difference ≥ 0.03 AUROC points
- **Rationale:** Domain adaptation should improve performance on specialized data

**H2 (Calibration):** TabPFN variants will show better calibration (lower ECE) than tree-based models.
- **Direction:** TabPFN ECE < GBDT ECE
- **Magnitude:** Expected difference ≥ 0.02 ECE points
- **Rationale:** Foundation models trained on diverse data should generalize better

**H3 (Fairness):** All models will exhibit fairness violations (EOD > 0.10) on COMPAS data.
- **Direction:** EOD > 0.10 for all models
- **Rationale:** Historical biases in criminal justice data are well-documented

**H4 (Fairness-Performance Tradeoff):** Fine-tuning will not significantly improve fairness metrics compared to baselines.
- **Direction:** No difference in EOD between fine-tuned TabPFN and XGBoost
- **Rationale:** Performance optimization doesn't necessarily address fairness

#### Secondary Hypotheses

**H5 (LocalPFN):** LocalPFN with retrieval will outperform zero-shot TabPFN but not exceed fine-tuned TabPFN.
- **Ordering:** Zero-shot < LocalPFN ≤ Fine-tuned

**H6 (Temporal Validation):** Performance will degrade on temporal holdout compared to cross-validation.
- **Direction:** Temporal AUROC < CV AUROC
- **Magnitude:** Expected drop ≥ 0.02 points

**H7 (Class Imbalance):** AUPRC will show larger differences between models than AUROC.
- **Direction:** AUPRC differences > AUROC differences
- **Rationale:** AUPRC is more sensitive to class imbalance

### 2.3 Null Hypotheses

**H0.1:** No difference in AUROC between fine-tuned TabPFN and best baseline (α = 0.05)

**H0.2:** No difference in calibration (ECE) between TabPFN and baselines (α = 0.05)

**H0.3:** No difference in fairness metrics (EOD) across models (α = 0.05)

---

## 3. Datasets and Samples

### 3.1 Primary Dataset: COMPAS Recidivism

**Source:** ProPublica's COMPAS investigation (Broward County, FL, 2013-2014)

**Sample Size:**
- Full dataset: n = 6,172 defendants
- Expected after filtering: n ≈ 6,000
- Train/test split: 80/20 stratified by outcome

**Inclusion Criteria:**
- Days between arrest and COMPAS screening ≤ 30
- Valid charge degree (M or F)
- Non-missing recidivism outcome
- Non-missing demographics (race, sex, age)

**Exclusion Criteria:**
- Missing COMPAS screening date
- Invalid or missing charge information
- Duplicate records (keep first occurrence)

**Target Variable:** Two-year general recidivism (binary)

**Features:** 14 baseline features
- Demographics: age, sex, race, age_cat
- Criminal history: juv_fel_count, juv_misd_count, juv_other_count, priors_count
- Current charge: c_charge_degree
- Exclude: COMPAS scores (to evaluate fairness-only prediction)

**Sensitive Attributes:**
- Race: African-American, Caucasian, Hispanic, Other
- Sex: Male, Female
- Age Category: Less than 25, 25-45, Greater than 45

### 3.2 Secondary Datasets

**UCI Communities & Crime** (if time permits)
- Sample size: n ≈ 1,994 communities
- Task: Violent crime rate regression
- Features: 122 socioeconomic/demographic variables

**Note:** NCVS and FBI UCR datasets require API access and are considered exploratory.

### 3.3 Sample Size Justification

**Power Analysis for Primary Comparisons:**

Using G*Power for paired model comparison:
- Effect size (Cohen's d): 0.3 (small-medium)
- α = 0.05 (two-tailed)
- Power (1-β) = 0.80
- Required sample size: n ≈ 90 for paired t-test

With n = 6,000 and 5-fold CV (1,200 per fold), we have adequate power to detect small-medium effects.

**For AUROC comparison (DeLong test):**
- Expected AUROC: 0.70-0.75
- Minimum detectable difference: 0.02-0.03
- Power: >0.90 with n = 6,000

---

## 4. Variables and Measures

### 4.1 Performance Metrics

**Primary Outcome:**
- **AUROC (Area Under ROC Curve):** Primary discrimination metric
  - Interpretation: Probability that a randomly selected recidivist has higher predicted risk than a randomly selected non-recidivist
  - Expected range: 0.65-0.75 (based on literature)
  - Minimum clinically meaningful difference: 0.03

**Secondary Outcomes:**
- **AUPRC (Area Under Precision-Recall Curve):** Important for imbalanced data
- **Brier Score:** Overall prediction accuracy (0 = perfect, 0.25 = random)
- **Log Loss:** Penalizes confident wrong predictions
- **Accuracy, Precision, Recall, F1:** Standard classification metrics

### 4.2 Calibration Metrics

**Primary:**
- **ECE (Expected Calibration Error):** Average absolute difference between confidence and accuracy
  - Calculation: 10 equal-frequency bins
  - Expected range: 0.02-0.10
  - Well-calibrated: ECE < 0.05

**Secondary:**
- **MCE (Maximum Calibration Error):** Worst-case calibration error
- **Brier Score Decomposition:** Calibration + refinement components
- **Calibration-in-the-large:** Overall calibration intercept
- **Calibration Slope:** Calibration regression slope (ideal = 1.0)

### 4.3 Fairness Metrics

**Primary:**
- **Equalized Odds Difference (EOD):** Max(|TPR_diff|, |FPR_diff|) across groups
  - Threshold: EOD > 0.10 indicates fairness concern
  - Expected: 0.10-0.20 based on ProPublica findings

**Secondary:**
- **Demographic Parity Difference (DPD):** Difference in positive prediction rates
- **Demographic Parity Ratio (DPR):** Ratio of prediction rates
- **Equalized Odds Ratio (EOR):** Ratio of TPR and FPR
- **Group-specific metrics:** TPR, FPR, PPV, NPV for each group

**Reference Group:**
- Race: Caucasian (majority group in dataset)
- Sex: Male (majority group)

### 4.4 Robustness Metrics

- **Temporal validation:** Performance on future data
- **Spatial validation:** Performance on held-out jurisdictions
- **Stability:** Performance variance across CV folds
- **Specification curve:** Performance across analytical choices

---

## 5. Statistical Analysis Plan

### 5.1 Model Comparison Strategy

#### Primary Comparisons

**Comparison 1: TabPFN Zero-shot vs Fine-tuned**
- Test: DeLong test for AUROC (paired)
- Test: McNemar's test for classification accuracy
- Effect size: Cohen's d for AUROC difference
- CI: 95% bootstrap confidence intervals (1,000 iterations)
- α = 0.05 (two-tailed)

**Comparison 2: Best TabPFN variant vs Best Baseline**
- Test: DeLong test for AUROC
- Test: Permutation test for Brier score
- Effect size: Risk difference, NNE
- Multiple comparison correction: Holm-Bonferroni

**Comparison 3: All models pairwise**
- Multiple testing: Benjamini-Hochberg FDR control (α = 0.05)
- Effect sizes: Cohen's d for all pairs
- Visualization: Heat map of pairwise differences

#### Statistical Tests Summary

| Comparison | Metric | Test | Correction |
|------------|--------|------|------------|
| TabPFN variants | AUROC | DeLong | None (pre-planned) |
| TabPFN vs Baselines | AUROC | DeLong | Holm |
| All pairwise | AUROC | DeLong | Benjamini-Hochberg |
| Classification | Accuracy | McNemar | Bonferroni |
| Calibration | ECE | Permutation | None |
| Fairness | EOD | Bootstrap CI | None |

### 5.2 Effect Sizes

**All comparisons must report:**
1. Point estimate of difference
2. 95% confidence interval
3. Standardized effect size (Cohen's d or equivalent)
4. Practical significance interpretation

**Interpretation Guidelines:**
- AUROC difference:
  - Small: 0.01-0.03
  - Medium: 0.03-0.05
  - Large: >0.05
- Cohen's d:
  - Small: 0.2
  - Medium: 0.5
  - Large: 0.8

### 5.3 Multiple Comparison Corrections

**Primary analyses:** Holm-Bonferroni correction (controls FWER)

**Secondary/exploratory analyses:** Benjamini-Hochberg correction (controls FDR at 0.05)

**Number of tests:**
- Model comparisons: 6 models × 5 models / 2 = 15 pairwise comparisons
- Fairness metrics: 4 sensitive attributes × 3-4 groups each ≈ 12 tests
- Total: ~30 tests → Holm-corrected α ≈ 0.05/30 ≈ 0.0017 for most conservative

**Reporting:**
- Report both uncorrected and corrected p-values
- State correction method used
- Interpret in context of correction

### 5.4 Confidence Intervals

**All metrics reported with 95% CIs using:**
- Bootstrap (non-parametric): 1,000 iterations minimum
- Stratified by outcome to maintain class proportions
- Percentile method for CI construction
- Random seed: 42 for reproducibility

### 5.5 Missing Data Handling

**Expected missing data:**
- COMPAS: Minimal (<1% after ProPublica filtering)
- Communities & Crime: LEMAS variables ~40% missing

**Missing Data Analysis:**
- Test for MCAR, MAR, MNAR patterns
- Chi-squared tests for categorical variables
- t-tests for continuous variables

**Handling Strategy:**
1. If MCAR and <5%: Complete case analysis (primary)
2. If MAR: Multiple imputation (sensitivity analysis)
3. If MNAR: Document and discuss limitations

**Sensitivity Analysis:**
- Compare results with complete cases vs imputed data
- Report missingness patterns in all tables

---

## 6. Subgroup Analyses

### 6.1 Pre-specified Subgroups

**Primary subgroups (confirmatory):**
1. **By Race:** African-American, Caucasian, Hispanic, Other
2. **By Sex:** Male, Female
3. **By Age Category:** <25, 25-45, >45

**Secondary subgroups (exploratory):**
4. **By Prior Record:** No priors, 1-3 priors, 4+ priors
5. **By Charge Severity:** Misdemeanor, Felony

### 6.2 Subgroup Analysis Plan

**For each subgroup:**
- Report all performance metrics (AUROC, AUPRC, etc.)
- Test for significant differences using interaction tests
- Calculate group-specific effect sizes
- Assess calibration within each group
- Test for fairness violations (EOD, DPD)

**Statistical Tests:**
- Interaction test: Logistic regression with group × model interaction
- Pairwise comparisons: DeLong test within each subgroup
- Multiple testing: Bonferroni correction for primary subgroups

**Reporting:**
- Table of metrics by group
- Forest plot of group-specific effect sizes
- Interaction p-values

### 6.3 Intersectional Analysis

**Intersectional subgroups (exploratory):**
- Race × Sex combinations (e.g., Black women, White men)
- Analyzed if cell sizes > 50

**Purpose:** Identify differential impacts on multiply-marginalized groups

**Reporting:**
- Mark as exploratory
- No corrections for multiple testing
- Hypothesis-generating for future research

---

## 7. Sensitivity Analyses

### 7.1 Pre-specified Sensitivity Analyses

**S1: Train/Test Split Ratio**
- Primary: 80/20 split
- Sensitivity: 70/30 and 90/10 splits
- Expected: Minimal impact on performance

**S2: Cross-Validation Folds**
- Primary: 5-fold CV
- Sensitivity: 3-fold and 10-fold
- Expected: Higher variance with 3-fold, negligible difference with 10-fold

**S3: Class Weighting**
- Primary: Balanced class weights
- Sensitivity: No weighting, inverse frequency weighting
- Expected: Improved recall with balancing, reduced precision

**S4: Feature Selection**
- Primary: All 14 features
- Sensitivity: Exclude age, exclude race (fairness-blind)
- Expected: Performance drop without age, minimal drop without race

**S5: Hyperparameter Tuning Trials**
- Primary: 20 Optuna trials
- Sensitivity: 10 and 50 trials
- Expected: Minimal difference (hyperparameters should converge)

**S6: Random Seeds**
- Primary: Seed = 42
- Sensitivity: Seeds 0, 1, 2, 3, 4
- Expected: Stability across seeds for well-tuned models
- Report: Mean and SD of metrics across seeds

**S7: Decision Threshold**
- Primary: 0.5 threshold
- Sensitivity: Youden's index, maximize F1, cost-weighted
- Expected: Threshold choice affects fairness metrics

### 7.2 Specification Curve Analysis

**Purpose:** Assess robustness across reasonable analytical choices

**Analytical dimensions:**
1. CV strategy (3-fold, 5-fold, 10-fold, temporal)
2. Class weighting (none, balanced, inverse)
3. Feature set (all, no age, no race, no demographics)
4. Performance metric (AUROC, AUPRC, F1)

**Analysis:**
- Estimate performance under all combinations
- Plot specification curve showing range of estimates
- Report median and range of estimates

**Interpretation:**
- Narrow range → Robust findings
- Wide range → Findings sensitive to choices

---

## 8. Deviations from Plan

### 8.1 Acceptable Deviations

**Deviations that do NOT require justification:**
- Adding exploratory analyses (marked as such)
- Additional visualization of results
- Expanding discussion of findings

**Deviations that REQUIRE justification:**
- Changing primary hypotheses
- Changing statistical tests
- Excluding pre-specified analyses
- Adding new pre-specified comparisons
- Changing significance thresholds

### 8.2 Documentation of Deviations

**All deviations must be documented in:**
- Research log (docs/research_log.md)
- Manuscript methods section
- Supplementary materials

**Template for deviation:**
```
Deviation Date: [DATE]
Original Plan: [What was planned]
Actual Analysis: [What was done instead]
Justification: [Why the deviation was necessary]
Impact: [How this affects interpretation]
```

---

## 9. Exploratory Analyses

### 9.1 Pre-specified Exploratory Analyses

**These are hypothesis-generating, not confirmatory:**

1. **Feature importance analysis**
   - SHAP values for tree-based models
   - Logistic regression coefficients
   - TabPFN attention weights (if available)

2. **Error analysis**
   - Confusion matrix analysis
   - False positive/negative case studies
   - Influential observations

3. **Calibration interventions**
   - Temperature scaling
   - Platt scaling
   - Isotonic regression

4. **Fairness interventions**
   - ThresholdOptimizer (Fairlearn)
   - Reductions approach
   - Cost-sensitive thresholds

5. **Learning curves**
   - Performance vs training set size
   - Sample efficiency comparison

6. **Multiverse analysis**
   - All combinations of reasonable choices
   - Specification curve analysis

### 9.2 Truly Exploratory Analyses

**Not pre-specified, to be clearly marked:**
- Any analyses suggested by reviewers
- Follow-up analyses based on unexpected findings
- Additional datasets beyond COMPAS
- New fairness metrics not listed above

**Reporting:**
- Clearly labeled "Exploratory" or "Post-hoc"
- Interpreted cautiously
- No strong conclusions drawn

---

## 10. Interim Analyses and Stopping Rules

### 10.1 Interim Analyses

**No interim analyses planned** except for:
1. Data quality checks (before any modeling)
2. Hyperparameter tuning (necessary for baseline quality)
3. Model debugging (necessary for valid implementation)

**None of these involve looking at test set performance.**

### 10.2 Stopping Rules

**No stopping rules.** All pre-specified analyses will be completed and reported regardless of results.

**Exceptions:**
- Technical failure (e.g., TabPFN won't install) → Document and proceed with available models
- Convergence failure → Try alternative optimizers, document if unresolved
- Computational infeasibility → Reduce CV folds or tuning trials, document change

---

## 11. Reporting Standards

### 11.1 Tables

**Table 1:** Sample characteristics
- Descriptive statistics for all variables
- By outcome (recidivist vs non-recidivist)
- Standardized mean differences
- Missing data patterns

**Table 2:** Model performance comparison
- All performance metrics with 95% CIs
- Statistical test results (p-values, effect sizes)
- Pairwise comparisons with corrections

**Table 3:** Fairness audit
- Group-specific metrics (TPR, FPR, PPV, NPV)
- Fairness disparities (EOD, DPD)
- Reference group comparisons
- Statistical significance

**Table 4:** Sensitivity analyses
- Primary result vs sensitivity results
- Range of estimates
- Robustness assessment

### 11.2 Figures

**Figure 1:** ROC and Precision-Recall curves
- All models on same plot
- 95% CIs shown as shaded regions
- AUROC/AUPRC values annotated

**Figure 2:** Calibration plots
- Reliability diagrams for all models
- Expected vs observed rates
- Confidence bands

**Figure 3:** Fairness visualizations
- Group-specific error rates
- Disparity metrics
- Fairness-accuracy tradeoff curves

**Figure 4:** Specification curve
- Performance across analytical choices
- Median and range of estimates
- Annotated with key decisions

### 11.3 Supplementary Materials

**Appendix A:** Complete statistical test results
- All pairwise comparisons
- Uncorrected and corrected p-values
- Full effect size estimates

**Appendix B:** Sensitivity analyses details
- Complete results for all sensitivity analyses
- Robustness checks

**Appendix C:** Fairness audit details
- Complete Aequitas audit results
- Intersectional analysis
- All group comparisons

**Appendix D:** Hyperparameter tuning
- Search spaces
- Tuning results
- Final hyperparameters

---

## 12. Transparency and Reproducibility

### 12.1 Code Availability

- All analysis code available on GitHub
- Notebooks documented with rationale for each step
- Environment specifications (requirements.txt, environment.yml)
- Docker container (if applicable)

### 12.2 Data Availability

- COMPAS: Publicly available from ProPublica
- Data cards documenting provenance
- Preprocessing scripts included
- No private/sensitive data committed

### 12.3 Pre-registration

- This analysis plan committed to GitHub before running final analyses
- Version controlled with timestamps
- Any deviations documented in research log

### 12.4 Reproducibility Checklist

- [ ] Random seeds fixed (42 throughout)
- [ ] Package versions locked (requirements.lock.txt)
- [ ] Complete analysis documented in notebooks
- [ ] Data preprocessing fully scripted
- [ ] Results regenerable with one command
- [ ] No manual steps required

---

## 13. Ethical Considerations

### 13.1 Use of COMPAS Data

**Ethical concerns:**
- Data reflects historical biases in criminal justice
- Potential for perpetuating discrimination
- Use as benchmark only, not for deployment

**Safeguards:**
- Explicit fairness evaluation
- Limitations clearly stated
- No deployment recommendations without stakeholder input

### 13.2 Reporting Obligations

**We commit to reporting:**
- All pre-specified analyses (positive or negative results)
- Fairness violations across all groups
- Limitations and potential harms
- Null findings (no suppression of non-significant results)

**We will NOT:**
- Cherry-pick favorable results
- Omit unfavorable fairness findings
- Make causal claims from predictive models
- Recommend deployment without ethical review

---

## 14. Timeline

**Phase 1 (Weeks 1-2):** Data exploration and preprocessing
**Phase 2 (Weeks 3-4):** Baseline model training and evaluation
**Phase 3 (Weeks 5-6):** TabPFN experiments
**Phase 4 (Weeks 7-8):** Fairness and calibration analysis
**Phase 5 (Weeks 9-10):** Sensitivity analyses and robustness checks
**Phase 6 (Weeks 11-12):** Statistical inference and reporting

---

## 15. Sign-off

**This analysis plan represents our best understanding of appropriate statistical methodology for this research question prior to observing final results.**

**Principal Investigator:** _________________ Date: _______

**Statistician/Methodologist:** _________________ Date: _______

**Version History:**
- v1.0 (2025-11-08): Initial pre-registration

---

## References

Angwin, J., Larson, J., Mattu, S., & Kirchner, L. (2016). Machine Bias. ProPublica.

Chouldechova, A. (2017). Fair prediction with disparate impact: A study of bias in recidivism prediction instruments. Big Data, 5(2), 153-163.

DeLong, E. R., DeLong, D. M., & Clarke-Pearson, D. L. (1988). Comparing the areas under two or more correlated receiver operating characteristic curves: a nonparametric approach. Biometrics, 837-845.

Kleinberg, J., Mullainathan, S., & Raghavan, M. (2017). Inherent trade-offs in the fair determination of risk scores. ITCS.

McNemar, Q. (1947). Note on the sampling error of the difference between correlated proportions or percentages. Psychometrika, 12(2), 153-157.
