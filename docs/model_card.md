# Model Card: TabPFN for Criminology

Following Mitchell et al. (2019) and guidance from the AI model card framework.

## Model Details

**Developed by:** [Research Team]
**Model date:** December 2024
**Model version:** 1.0
**Model type:** Transformer-based tabular foundation model (TabPFN v2) with fine-tuning and retrieval augmentation
**License:** MIT
**Contact:** [Email]

### Model Description

This model card covers three variants of TabPFN applied to criminology datasets:

1. **TabPFN (Zero-shot):** Pre-trained TabPFN v2 used for in-context learning without gradient updates
2. **TabPFN (Fine-tuned):** End-to-end supervised fine-tuning on downstream criminology tasks
3. **LocalPFN:** Retrieval-augmented variant that finds K nearest neighbors and optionally fine-tunes on local context

All variants are built on the TabPFN architecture [Hollmann et al., 2023], which is a transformer trained on synthetic tabular datasets to perform few-shot classification and regression.

## Intended Use

### Primary Intended Uses

- **Research:** Benchmarking tabular foundation models on criminology tasks
- **Development:** Prototyping predictive models for recidivism, crime forecasting, and victimization analysis
- **Education:** Teaching machine learning fairness and calibration in high-stakes contexts

### Primary Intended Users

- Criminology researchers
- Data scientists in criminal justice agencies (with appropriate oversight and validation)
- ML fairness researchers
- Policy analysts

### Out-of-Scope Uses

**DO NOT USE for:**
- Automated decision-making without human oversight (e.g., automatic denial of parole)
- Predicting individual propensity for crime without considering context and rehabilitation
- Racial profiling or discriminatory policing
- Deployment in production without jurisdiction-specific validation and stakeholder engagement
- Uses that violate civil rights or due process

## Factors

### Relevant Factors

**Groups:** Performance and fairness vary by:
- Race (African-American, Caucasian, Hispanic, Asian, Other)
- Sex (Male, Female)
- Age (categories: <25, 25-45, >45)

**Context:**
- Geographic jurisdiction (county, state)
- Time period (temporal drift)
- Data quality (missingness, measurement error)
- Base rates (prevalence of outcome varies by context)

### Evaluation Factors

We evaluate across sensitive groups and assess:
- **Performance:** AUROC, AUPRC, log loss, Brier score
- **Calibration:** ECE, MCE, reliability diagrams
- **Fairness:** Equalized odds difference, demographic parity difference, TPR/FPR gaps

## Metrics

### Performance Metrics

| Dataset | Model | AUROC | AUPRC | Brier | ECE |
|---------|-------|-------|-------|-------|-----|
| COMPAS | TabPFN (zero-shot) | [X.XX] | [X.XX] | [X.XX] | [X.XX] |
| COMPAS | TabPFN (fine-tuned) | [X.XX] | [X.XX] | [X.XX] | [X.XX] |
| COMPAS | LocalPFN | [X.XX] | [X.XX] | [X.XX] | [X.XX] |

[Additional rows for Communities & Crime, NCVS, UCR]

### Fairness Metrics

| Dataset | Model | Equalized Odds Diff | Demographic Parity Diff | TPR Ratio (min/max) |
|---------|-------|---------------------|-------------------------|---------------------|
| COMPAS | TabPFN (zero-shot) | [X.XX] | [X.XX] | [X.XX] |
| COMPAS | TabPFN (fine-tuned) | [X.XX] | [X.XX] | [X.XX] |
| COMPAS | LocalPFN | [X.XX] | [X.XX] | [X.XX] |

**Interpretation:**
- Equalized odds difference >0.10 indicates meaningful fairness concern
- TPR ratio <0.80 or >1.25 suggests disparate impact
- All models exhibit [some degree of] bias; post-processing may be required

### Decision Thresholds

Default threshold: 0.5
Recommended approach: **Stakeholder-defined thresholds based on error costs**

Example alternative thresholds:
- High recall (minimize false negatives): threshold = 0.3
- High precision (minimize false positives): threshold = 0.7
- Equalized odds (fairness-optimized): threshold varies by group [requires post-processing]

## Training Data

### Datasets

1. **COMPAS (ProPublica):** 6,000+ defendants, Broward County FL, 2013-2014
2. **UCI Communities & Crime:** 1,994 US communities, 1990 Census + 1995 UCR
3. **NCVS:** National Crime Victimization Survey, 2010-2023 (via BJS API)
4. **FBI UCR:** Uniform Crime Reporting, agency-level data (via Crime Data Explorer API)

### Preprocessing

- ProPublica filtering applied to COMPAS
- Missing data: median imputation or row deletion (configurable)
- Categorical encoding: one-hot encoding
- Feature scaling: optional standardization (for logistic baselines)
- Exclusions: COMPAS risk scores excluded for fairness-only prediction

## Evaluation Data

- **COMPAS:** 5-fold stratified cross-validation + subject-level grouping
- **Communities & Crime:** Spatial K-fold (grouped by state)
- **NCVS:** Temporal holdout (train 2010-2020, test 2021-2023)
- **UCR:** Jurisdictional holdout (20% agencies)

Bootstrap confidence intervals (n=1,000) for all metrics.

## Ethical Considerations

### Risks and Harms

**Allocation harms:**
- False positives: Individuals incorrectly predicted as high-risk may face harsher treatment (e.g., detention, surveillance)
- False negatives: Individuals incorrectly predicted as low-risk may not receive needed interventions (e.g., rehabilitation services)

**Representational harms:**
- Model may perpetuate stereotypes if training data reflects historical biases in policing and adjudication
- Overemphasis on demographic features (race, sex, age) can reinforce discriminatory narratives

**Feedback loops:**
- If model predictions inform criminal justice decisions (e.g., bail, sentencing), outcomes may feed back into future training data, amplifying biases

### Mitigation Strategies

1. **Fairness audits:** Comprehensive evaluation across sensitive groups (Fairlearn, Aequitas)
2. **Calibration assessment:** Ensure predicted probabilities are reliable for decision-making
3. **Stakeholder engagement:** Consult with judges, probation officers, defense attorneys, and community members
4. **Human oversight:** Models should support, not replace, human judgment
5. **Transparency:** Provide explanations (SHAP, feature attributions) for predictions
6. **Redress mechanisms:** Establish appeals process for individuals affected by predictions

### Use Case Restrictions

- **Require human review** for all high-stakes decisions
- **Conduct local validation** before deployment in new jurisdictions
- **Monitor for drift** and retrain/recalibrate periodically
- **Respect due process** and provide explanations to affected individuals

## Caveats and Recommendations

### Known Limitations

1. **Dataset bias:** Training data reflects historical inequities in criminal justice system
2. **Temporal drift:** Model performance may degrade as crime patterns shift
3. **Spatial heterogeneity:** Model trained on one jurisdiction may not generalize to another
4. **Class imbalance:** Rare events (violent recidivism) are harder to predict
5. **Feature availability:** Some jurisdictions lack detailed criminal history data
6. **Intersectional fairness:** Limited analysis of intersectional groups (e.g., Black women) due to sample size

### Recommendations

- **Do not deploy without validation:** Test on local data and assess fairness before use
- **Monitor performance over time:** Retrain or recalibrate as needed
- **Use in conjunction with other tools:** Risk assessments are one input among many
- **Prioritize rehabilitation:** Predictive models should inform supportive interventions, not punitive measures
- **Respect privacy:** Ensure data use complies with privacy laws and ethical guidelines

## References

- Hollmann, N., et al. (2023). TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second. arXiv:2207.01848.
- Mitchell, M., et al. (2019). Model Cards for Model Reporting. FAT* '19.
- Angwin, J., et al. (2016). Machine Bias. ProPublica.
- Gebru, T., et al. (2021). Datasheets for Datasets. CACM.

## Changelog

- **v1.0 (Dec 2024):** Initial release with COMPAS, Communities & Crime, NCVS, UCR evaluations
