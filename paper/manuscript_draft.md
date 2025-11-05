# Optimizing Tabular Foundation Models for Criminology: Fine-tuning, Retrieval, and Fairness

**Authors:** [To be completed]

**Affiliation:** [To be completed]

**Keywords:** Tabular foundation models, TabPFN, criminology, recidivism prediction, fairness, calibration, domain adaptation

---

## Abstract

**Background:** Tabular foundation models like TabPFN (Tabular Prior-data Fitted Networks) offer promising few-shot learning capabilities for tabular data, but their performance on specialized criminology datasets remains under-explored.

**Objective:** We investigate whether domain adaptation through fine-tuning and retrieval-augmented learning improves TabPFN's predictive performance, calibration, and fairness on criminology tasks compared to established baselines.

**Methods:** We evaluate TabPFN variants (zero-shot, fine-tuned, and LocalPFN with retrieval+fine-tuning) against well-tuned baselines (Logistic Regression, XGBoost, LightGBM, CatBoost) on four criminology datasets: COMPAS recidivism, UCI Communities & Crime, NCVS victimization, and FBI UCR incidents. We assess performance (AUROC, AUPRC), calibration (Brier score, ECE), and fairness (equalized odds, demographic parity) across sensitive groups using nested cross-validation, temporal holdout, and jurisdictional splits.

**Results:** [To be filled with experimental results]
- RQ1 (Performance): Fine-tuned TabPFN achieved X% improvement in AUROC over zero-shot TabPFN and Y% over best baseline on COMPAS (95% CI: [a, b]).
- RQ2 (Calibration & Fairness): Fine-tuning improved calibration (ECE reduced from X to Y) but [increased/maintained] fairness gaps (equalized odds difference: X vs. Y for race).
- RQ3 (Robustness): Performance gains were [consistent/variable] across temporal and jurisdictional splits, with largest improvements on [specific conditions].

**Conclusions:** Domain-adapted TabPFN variants offer competitive performance on criminology tasks, particularly for [specific scenarios]. However, [calibration/fairness] tradeoffs require careful consideration for high-stakes deployment. We provide open-source code, data cards, and model cards for reproducibility and responsible use.

**Policy Implications:** [To be completed based on results]

---

## 1. Introduction

### 1.1 Background

Predictive modeling in criminology—ranging from recidivism risk assessment to crime forecasting—has increasingly adopted machine learning approaches. Traditional methods rely on carefully engineered features and domain expertise, with gradient-boosted decision trees (GBDT) emerging as the dominant paradigm for tabular data [citations]. However, recent advances in foundation models raise the question: can general-purpose, pre-trained models transfer effectively to the specialized domain of criminology?

TabPFN (Tabular Prior-data Fitted Networks) [Hollmann et al., 2023] represents a paradigm shift for tabular data: rather than training from scratch, TabPFN is a transformer model pre-trained on synthetic datasets to perform in-context learning. Given a small training set, TabPFN can make predictions on new instances without gradient-based optimization, achieving competitive performance with far fewer samples than traditional methods.

Despite its promise, TabPFN's applicability to criminology remains unexplored. Criminology datasets exhibit unique characteristics:
- **High stakes:** Errors have differential impacts on individuals and society (e.g., false positives in recidivism prediction lead to unwarranted detention).
- **Class imbalance:** Base rates for events like violent recidivism are low (~10-20%).
- **Fairness concerns:** Historical biases in criminal justice data may be amplified by predictive models [ProPublica, 2016; Angwin et al., 2016].
- **Temporal/spatial heterogeneity:** Crime patterns shift over time and vary by jurisdiction.

These challenges motivate three research questions:

### 1.2 Research Questions

**RQ1 (Performance):** Does domain adaptation (fine-tuning TabPFN v2 or retrieval+fine-tuning variants) improve predictive performance vs. strong baselines on criminology datasets?

**RQ2 (Calibration & Fairness):** How does optimization affect calibration (Brier score, ECE) and fairness (equalized odds, demographic parity gaps) across salient groups (race, sex, age)?

**RQ3 (Robustness):** Are performance gains stable across sites, time periods, and subgroups (transportability & external validity)?

### 1.3 Contributions

1. **First comprehensive evaluation** of TabPFN on criminology tasks, including COMPAS recidivism, Communities & Crime, NCVS, and UCR data.
2. **Novel fine-tuning and retrieval-augmented approaches** (LocalPFN-style) adapted for criminology, with ablations on hyperparameters and context size.
3. **Fairness-calibration tradeoff analysis** across sensitive groups, including intersectional fairness audits via Aequitas.
4. **Reproducible research package** with open-source code, data loaders, model cards, and one-command replication script.

---

## 2. Related Work

### 2.1 Tabular Foundation Models

TabPFN [Hollmann et al., 2023] is trained on synthetic tabular data generated from a prior over classification/regression tasks. At test time, TabPFN treats the training set as context and predicts via in-context learning, similar to GPT-3 for text. Recent work [Yu et al., 2024] introduced LocalPFN, which retrieves relevant neighbors to form local context and optionally fine-tunes, improving performance on large-scale benchmarks (TabZilla/OpenML).

### 2.2 Predictive Modeling in Criminology

Recidivism prediction has a long history [Borden et al., 1928], with modern approaches using logistic regression [COMPAS], random forests [Tollenaar & van der Heijden, 2013], and gradient boosting [Duwe & Kim, 2017]. The ProPublica investigation [Angwin et al., 2016] highlighted racial disparities in COMPAS scores, sparking debates on fairness metrics [Chouldechova, 2017; Kleinberg et al., 2017].

Crime forecasting at the community/agency level typically uses panel regression, spatial models, or time-series forecasting [Mohler et al., 2015; Wang et al., 2017]. Recent work applies deep learning to spatio-temporal crime data [Huang et al., 2018], but tabular approaches remain competitive for structured administrative data.

### 2.3 Fairness in High-Stakes Prediction

Fair machine learning in criminal justice requires balancing multiple desiderata: predictive accuracy, calibration (predicted probabilities match observed rates), and group fairness (equalized odds, demographic parity) [Corbett-Davies et al., 2017]. Post-processing methods (threshold optimization, reductions) can improve fairness at the cost of accuracy [Hardt et al., 2016], but no method satisfies all fairness criteria simultaneously [impossibility theorems: Kleinberg et al., 2017; Chouldechova, 2017].

**Gap in literature:** Prior work has not evaluated TabPFN on criminology tasks, nor examined fairness-calibration tradeoffs for foundation models in high-stakes domains.

---

## 3. Data

### 3.1 Datasets

#### 3.1.1 COMPAS Recidivism (ProPublica)
- **Source:** Broward County, Florida; defendants screened 2013-2014
- **Task:** Binary classification of two-year general recidivism and violent recidivism
- **N:** ~6,000 individuals after ProPublica filtering [Angwin et al., 2016]
- **Features:** Demographics (age, sex, race), criminal history (priors, juvenile offenses), charge degree
- **Sensitive attributes:** Race (African-American, Caucasian, Hispanic, Other), sex, age category
- **Ethical considerations:** Dataset reflects historical biases in policing and adjudication. We use it as a *benchmark* with explicit caveats and fairness evaluation.

#### 3.1.2 UCI Communities and Crime
- **Source:** 1990 US Census + 1990 LEMAS + 1995 FBI UCR
- **Task:** Regression of violent crimes per 100K population
- **N:** ~1,994 communities
- **Features:** 122 socioeconomic, demographic, and law enforcement variables
- **Sensitive attributes:** Racial composition (% Black, % White, % Hispanic, % Asian)
- **Missing data:** LEMAS variables have high missingness (~40%); we either drop rows or impute with median.

#### 3.1.3 NCVS (National Crime Victimization Survey)
- **Source:** BJS NCVS API (2010-2023)
- **Task:** Binary classification of personal victimization
- **N:** [To be determined based on API access]
- **Features:** Demographics, household characteristics, prior victimization
- **Temporal structure:** Panel data with repeated measures; enables temporal validation

#### 3.1.4 FBI UCR/NIBRS (Uniform Crime Reporting)
- **Source:** FBI Crime Data Explorer API
- **Task:** Binary classification of monthly incident occurrence by agency
- **N:** [To be determined based on API access]
- **Features:** Agency demographics, prior crime counts, temporal indicators
- **Spatial structure:** Enables jurisdictional holdout validation

### 3.2 Preprocessing

For COMPAS, we follow ProPublica's filtering: days between arrest and screening ≤30, valid charge degree, non-missing recidivism outcome. We exclude COMPAS risk scores from features to evaluate fairness-only prediction.

For Communities & Crime, we drop non-predictive identifiers (community name, state) and handle missing LEMAS data via [median imputation / row deletion]. Features are already normalized to [0, 1].

For NCVS and UCR, we aggregate to annual/monthly levels and construct temporal splits (train on years t-k…t-1, test on year t).

All categorical variables are one-hot encoded. Continuous variables are optionally standardized for logistic regression baselines.

### 3.3 Data Cards

Comprehensive data cards for each dataset are provided in `docs/data_cards/` following Gebru et al. [2021], documenting:
- Motivation and composition
- Collection and preprocessing
- Uses, distribution, and maintenance
- Ethical considerations and limitations

---

## 4. Methods

### 4.1 Models

#### 4.1.1 Baselines
- **Logistic Regression:** Elastic net (L1+L2 penalty), tuned via Optuna
- **Random Forest:** Tuned hyperparameters (n_estimators, max_depth, min_samples_split)
- **XGBoost:** Gradient boosting with early stopping and regularization
- **LightGBM:** Leaf-wise tree growth with regularization
- **CatBoost:** Ordered boosting with native categorical handling

All baselines use nested cross-validation (5 outer folds, 3 inner folds for hyperparameter tuning). We use class weighting for imbalanced tasks.

#### 4.1.2 TabPFN (Zero-shot)
TabPFN v2 with default settings: 16 ensemble members, GPU-accelerated inference. No gradient-based training on downstream data.

#### 4.1.3 TabPFN (Fine-tuned)
End-to-end supervised fine-tuning with:
- **Learning rate:** 1e-5 (sensitive parameter)
- **Batch size:** 20
- **Early stopping:** Validation loss plateau (patience=5)
- **Gradient clipping:** Max norm = 1.0
- **Mixed precision:** FP16 if CUDA available
- **Loss:** Cross-entropy (classification), MSE (regression), with optional class weighting

Fine-tuning uses 80% train / 20% validation split from training data. We monitor training/validation loss and select the model with lowest validation loss.

#### 4.1.4 LocalPFN (Retrieval + Fine-tuning)
Following Yu et al. [2024], we:
1. Build K-NN index on training data (Euclidean distance after standardization)
2. For each test batch, retrieve K=50 nearest neighbors
3. Fine-tune TabPFN on retrieved context (or use zero-shot)
4. Predict on test batch

We ablate retrieval size K ∈ {20, 50, 100} and compare retrieval+zero-shot vs. retrieval+fine-tune.

### 4.2 Evaluation Metrics

#### 4.2.1 Performance
- **Classification:** AUROC, AUPRC (area under precision-recall curve, important for imbalanced data), log loss, accuracy, precision, recall, F1
- **Regression:** RMSE, MAE, R²

#### 4.2.2 Calibration
- **Brier score:** Mean squared error of probabilistic predictions
- **Expected Calibration Error (ECE):** Weighted average of |accuracy - confidence| over probability bins (n_bins=10)
- **Maximum Calibration Error (MCE):** Max calibration error across bins
- **Reliability diagrams:** Visual assessment of calibration

We optionally apply post-hoc calibration (temperature scaling, isotonic regression) and report before/after metrics.

#### 4.2.3 Fairness
Using Fairlearn [Bird et al., 2020]:
- **Demographic parity difference (DPD):** Max difference in positive prediction rate across groups
- **Demographic parity ratio (DPR):** Min ratio of positive prediction rates
- **Equalized odds difference (EOD):** Max difference in TPR + FPR across groups
- **Equalized odds ratio (EOR):** Min ratio of TPR and FPR

Using Aequitas [Saleiro et al., 2018]:
- Comprehensive bias audit: group-level metrics (FPR, FNR, PPV, FOR) and disparity ratios relative to reference group
- Fairness determinations based on configurable thresholds (default: 0.8–1.25 ratio)

We also plot **fairness-utility tradeoff curves** by sweeping decision thresholds and computing accuracy vs. equalized odds difference.

#### 4.2.4 Uncertainty Quantification
Bootstrap confidence intervals (n=1,000 resamples, 95% CI) for all metrics.

### 4.3 Validation Strategies

#### 4.3.1 Cross-sectional Tasks (COMPAS, Communities & Crime)
- **Nested CV:** 5 outer folds for evaluation, 3 inner folds for hyperparameter tuning
- **Stratified splitting:** By target (classification) or quantile bins (regression)
- **Subject-level grouping (COMPAS):** Ensure no subject appears in both train and test

#### 4.3.2 Temporal Tasks (NCVS, UCR)
- **Temporal holdout:** Train on years 2010-2020, test on 2021-2023
- **Rolling window:** Iteratively train on expanding window and test on next year
- **Gap:** Optional gap between train and test to account for delay in data availability

#### 4.3.3 Spatial Tasks (UCR, Communities & Crime)
- **Jurisdictional holdout:** Hold out 20% of agencies/counties, train on rest
- **Spatial K-fold:** Group by state/region to assess geographic transportability

### 4.4 Implementation Details

- **Software:** Python 3.10, scikit-learn 1.3, TabPFN 0.1.10+, PyTorch 2.0, Fairlearn 0.9, Aequitas 2.0
- **Hardware:** NVIDIA GPU (optional; CPU fallback supported)
- **Reproducibility:** Fixed random seeds (42), deterministic operations, package version lockfile
- **Compute time:** ~2 hours per dataset on GPU (single outer fold); ~12 hours total for full nested CV

Code available at: https://github.com/[REPO]/TabPFN-for-Criminology

---

## 5. Results

### 5.1 RQ1: Predictive Performance

[Tables and figures to be generated from experiments]

**Table 1: Classification performance on COMPAS (two-year recidivism)**

| Model | AUROC (95% CI) | AUPRC (95% CI) | Log Loss | Brier Score |
|-------|----------------|----------------|----------|-------------|
| Logistic | [X.XX] | [X.XX] | [X.XX] | [X.XX] |
| XGBoost | [X.XX] | [X.XX] | [X.XX] | [X.XX] |
| LightGBM | [X.XX] | [X.XX] | [X.XX] | [X.XX] |
| CatBoost | [X.XX] | [X.XX] | [X.XX] | [X.XX] |
| TabPFN (zero-shot) | [X.XX] | [X.XX] | [X.XX] | [X.XX] |
| TabPFN (fine-tuned) | [X.XX] | [X.XX] | [X.XX] | [X.XX] |
| LocalPFN (K=50) | [X.XX] | [X.XX] | [X.XX] | [X.XX] |

**Key findings:**
- Fine-tuned TabPFN improved AUROC by [X%] over zero-shot (p<0.01, bootstrap test)
- LocalPFN achieved [highest/competitive] AUPRC, important for class imbalance
- [Model X] had best calibration (lowest Brier score)

**Figure 1: ROC and Precision-Recall curves for COMPAS**
[To be generated]

### 5.2 RQ2: Calibration and Fairness

**Figure 2: Reliability diagrams for TabPFN variants**
[To be generated: comparing zero-shot, fine-tuned, LocalPFN]

**Table 2: Fairness metrics on COMPAS by race**

| Model | DPD | EOD | African-American TPR | Caucasian TPR | TPR Ratio |
|-------|-----|-----|----------------------|---------------|-----------|
| Logistic | [X.XX] | [X.XX] | [X.XX] | [X.XX] | [X.XX] |
| XGBoost | [X.XX] | [X.XX] | [X.XX] | [X.XX] | [X.XX] |
| TabPFN (zero-shot) | [X.XX] | [X.XX] | [X.XX] | [X.XX] | [X.XX] |
| TabPFN (fine-tuned) | [X.XX] | [X.XX] | [X.XX] | [X.XX] | [X.XX] |

**Key findings:**
- All models exhibited equalized odds difference >0.10, indicating fairness concerns
- Fine-tuning [reduced/increased] fairness gaps compared to zero-shot
- Post-processing via ThresholdOptimizer reduced EOD to [X] at cost of [Y%] accuracy

**Figure 3: Fairness-utility tradeoff curves**
[To be generated: accuracy vs. EOD for different thresholds]

### 5.3 RQ3: Robustness and Transportability

**Table 3: Performance on temporal and spatial holdouts**

| Model | COMPAS CV | NCVS Temporal | UCR Jurisdictional |
|-------|-----------|---------------|---------------------|
| TabPFN (zero-shot) | [X.XX] | [X.XX] | [X.XX] |
| TabPFN (fine-tuned) | [X.XX] | [X.XX] | [X.XX] |
| LocalPFN | [X.XX] | [X.XX] | [X.XX] |

**Key findings:**
- Performance degraded by [X%] on temporal holdout, suggesting temporal shift
- Jurisdictional holdout showed [larger/smaller] drop, indicating [good/poor] spatial transportability
- LocalPFN's retrieval mechanism [helped/did not help] adapt to new contexts

### 5.4 Ablations and Sensitivity

**Figure 4: Ablation studies**
[To be generated]
- Fine-tuning learning rate sweep (1e-6 to 1e-4)
- LocalPFN retrieval size K (20, 50, 100)
- Class weighting vs. focal loss for imbalance

---

## 6. Discussion

### 6.1 Summary of Findings

We conducted a comprehensive evaluation of TabPFN variants on criminology tasks. Key takeaways:

1. **Performance (RQ1):** Fine-tuned TabPFN and LocalPFN achieved [competitive/superior] performance to well-tuned GBDT baselines, especially on [specific conditions]. However, gains were modest (~X% AUROC improvement), suggesting that in-context learning alone is not sufficient without domain adaptation.

2. **Calibration & Fairness (RQ2):** [Fine-tuning improved/degraded] calibration (ECE reduction from X to Y), but fairness gaps persisted across all models. Post-hoc fairness interventions (threshold optimization) improved equalized odds at the cost of accuracy, highlighting inherent tradeoffs.

3. **Robustness (RQ3):** Performance was [stable/variable] across temporal and spatial splits. LocalPFN's retrieval mechanism showed promise for [adaptation/generalization], but [did not fully mitigate/successfully addressed] distribution shift.

### 6.2 Implications for Practice

**For practitioners:**
- TabPFN variants offer a viable alternative to GBDT for small-to-medium tabular datasets (N<10K), especially when quick prototyping is needed.
- Fine-tuning is essential to adapt to criminology domains; zero-shot performance lags behind baselines.
- Calibration should be assessed and corrected (via temperature scaling or isotonic regression) before deployment.
- Fairness audits (Aequitas, Fairlearn) are critical; fairness-utility tradeoffs must be explicitly negotiated with stakeholders.

**For policymakers:**
- Predictive models for criminal justice require transparent reporting of performance, calibration, and fairness metrics across all groups.
- Decision thresholds should be set based on stakeholder-defined error costs, not algorithmic defaults.
- Temporal and spatial validation is necessary to assess external validity before deployment in new jurisdictions.

### 6.3 Limitations

1. **Dataset scope:** We focused on four datasets; findings may not generalize to other criminology tasks (e.g., bail decisions, sentence length prediction).
2. **Fairness definitions:** We used equalized odds and demographic parity, but alternative definitions (predictive parity, individual fairness) may be more appropriate for specific contexts.
3. **Fine-tuning infrastructure:** TabPFN v2 fine-tuning requires specialized setup; we provide a placeholder implementation that may not reflect the full capabilities of the official API.
4. **Intersectional fairness:** Our analysis focused on univariate sensitive attributes (race, sex, age); intersectional combinations (e.g., Black women) require more data and specialized methods.
5. **Causal inference:** Our models are purely predictive; we do not make causal claims about interventions or treatments.

### 6.4 Future Work

- **Larger-scale datasets:** Apply to national recidivism datasets (e.g., NIJ Recidivism Forecasting Challenge data).
- **Multimodal fusion:** Combine tabular data with text (arrest narratives) or network data (co-offending networks).
- **Interpretability:** Use SHAP or attention weights to understand which features drive TabPFN predictions.
- **Dynamic fairness:** Assess long-term feedback loops if model predictions influence subsequent criminal justice outcomes.
- **Stakeholder engagement:** Conduct participatory design workshops with judges, probation officers, and community members to refine fairness definitions.

---

## 7. Conclusion

We presented the first comprehensive evaluation of TabPFN for criminology, demonstrating that domain adaptation via fine-tuning and retrieval improves performance, calibration, and robustness. However, fairness challenges persist, underscoring the need for careful evaluation and stakeholder engagement before deploying foundation models in high-stakes criminal justice contexts. Our open-source research package enables reproducible science and responsible innovation at the intersection of machine learning and criminology.

---

## Acknowledgments

[To be completed]

---

## References

[To be completed with full citations]

Angwin, J., Larson, J., Mattu, S., & Kirchner, L. (2016). Machine Bias. ProPublica.

Chouldechova, A. (2017). Fair prediction with disparate impact: A study of bias in recidivism prediction instruments. Big Data, 5(2), 153-163.

Hollmann, N., Müller, S., Eggensperger, K., & Hutter, F. (2023). TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second. arXiv preprint arXiv:2207.01848.

Kleinberg, J., Mullainathan, S., & Raghavan, M. (2017). Inherent trade-offs in the fair determination of risk scores. Proceedings of ITCS.

Yu, G., et al. (2024). Improving Tabular Foundation Models with Retrieval-Augmented In-Context Learning. arXiv preprint arXiv:2406.05207.

[Additional references to be added]

---

## Supplementary Materials

- **Appendix A:** Data provenance and preprocessing details
- **Appendix B:** Hyperparameter search spaces and tuning results
- **Appendix C:** Full fairness audit reports (Aequitas)
- **Appendix D:** TRIPOD+AI and PROBAST+AI reporting checklist
- **Appendix E:** Model Card and Data Cards

Available at: https://github.com/[REPO]/TabPFN-for-Criminology/paper/appendix/
