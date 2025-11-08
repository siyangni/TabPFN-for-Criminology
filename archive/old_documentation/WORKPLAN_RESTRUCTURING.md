# Comprehensive Workplan: Repository Restructuring for Criminology Research Methods Publication

**Date:** 2025-11-08
**Objective:** Transform this repository from an ML-focused automated pipeline to an interactive, methodologically rigorous criminology research package suitable for publication in a criminology research methods journal.

---

## Executive Summary

### Current State
- **Structure:** Production-quality Python codebase (7,100+ lines)
- **Design Philosophy:** Automated script execution, minimal user interaction
- **Focus:** Machine learning performance metrics (AUROC, AUPRC)
- **Workflow:** Master scripts that run entire pipelines (`run_all_experiments.py`)
- **Format:** Zero Jupyter notebooks, all Python scripts
- **Target Audience:** ML researchers, data scientists

### Target State
- **Structure:** Interactive Jupyter notebook-based research workflow
- **Design Philosophy:** Transparent, exploratory, step-by-step analysis
- **Focus:** Methodological rigor, statistical validity, ethical considerations
- **Workflow:** Modular notebooks with narrative explanations at each step
- **Format:** Jupyter notebooks for analysis, Python modules for reusable functions
- **Target Audience:** Criminology researchers, methodologists, domain experts

---

## Part 1: Methodological Framework Enhancement for Publishability

### 1.1 Shift from ML Performance to Research Methodology

#### Current Issues
- Heavy emphasis on predictive metrics (AUROC, AUPRC) without sufficient context
- Insufficient discussion of research design choices and their implications
- Limited statistical inference beyond bootstrap CIs
- Sparse documentation of analytic decisions and their rationale

#### Proposed Changes

**1.1.1 Add Pre-Registration/Analysis Plan**
- Create `docs/analysis_plan.md` documenting:
  - A priori hypotheses (beyond RQ1-3)
  - Planned statistical tests with power analysis
  - Decision rules for model selection
  - Sensitivity analyses to be conducted
  - Criteria for interpreting effect sizes
  - Pre-specified subgroup analyses

**1.1.2 Enhanced Statistical Inference**
- Replace simple bootstrap CIs with comprehensive statistical testing:
  - McNemar's test for paired model comparisons
  - DeLong test for AUROC comparisons
  - Permutation tests for fairness metrics
  - Multiple comparison corrections (Bonferroni, Holm-Bonferroni)
  - Effect size reporting (Cohen's d, Cramér's V)
  - Statistical power analysis for key comparisons

**1.1.3 Robustness and Sensitivity Analysis**
- Add systematic sensitivity analyses:
  - Varying class imbalance thresholds
  - Different train/test split ratios
  - Alternative missing data handling strategies
  - Sensitivity to outliers and influential observations
  - Stability across random seeds (beyond single seed)
  - Cross-validation scheme sensitivity (k-fold, stratified, grouped)

**1.1.4 Measurement Validity and Reliability**
- Add comprehensive data quality assessment:
  - Missing data patterns analysis (MCAR, MAR, MNAR)
  - Inter-rater reliability for coded variables
  - Measurement error quantification
  - Construct validity evidence
  - Discriminant and convergent validity tests

### 1.2 Enhanced Ethical and Domain Considerations

#### Current Issues
- Brief ethical disclaimers but limited substantive engagement
- Insufficient discussion of stakeholder impacts
- Limited connection to criminological theory
- Sparse discussion of policy implications

#### Proposed Changes

**1.2.1 Comprehensive Ethics Documentation**
- Create `docs/ethical_framework.md`:
  - Detailed stakeholder impact analysis
  - Error cost asymmetry discussion (FP vs FN consequences)
  - Historical bias documentation
  - Potential for harm assessment
  - Mitigation strategies
  - Community engagement approach
  - Informed consent considerations (if applicable)

**1.2.2 Theoretical Grounding**
- Add `docs/theoretical_framework.md`:
  - Criminological theory connections (e.g., life-course theory, social disorganization)
  - Prior literature on recidivism/crime prediction
  - Conceptual model of risk factors
  - Theory-driven feature selection rationale
  - Alternative theoretical perspectives considered

**1.2.3 Policy Implications Framework**
- Create `docs/policy_implications.md`:
  - Decision-making contexts for model use
  - Threshold selection guidance for practitioners
  - Implementation considerations
  - Monitoring and auditing recommendations
  - Appeal and recourse mechanisms
  - Training requirements for users

### 1.3 Enhanced Transparency and Replicability

#### Current Issues
- Code is reproducible but lacks narrative explanation
- Limited documentation of failed experiments or negative results
- Insufficient detail on data preprocessing decisions

#### Proposed Changes

**1.3.1 Research Transparency**
- Create `docs/research_log.md`:
  - Chronological log of all analyses conducted (including failures)
  - Deviations from analysis plan with justification
  - Unexpected findings and their investigation
  - Researcher degrees of freedom exercised
  - Alternative approaches considered and rejected

**1.3.2 Detailed Data Provenance**
- Expand data cards to include:
  - Complete data collection protocols
  - Sampling strategy and population definition
  - Response rates and non-response analysis
  - Data validation procedures
  - Quality control checks
  - Data cleaning decision log
  - Version control for dataset changes

**1.3.3 Computational Reproducibility**
- Add `docs/computational_environment.md`:
  - Hardware specifications
  - Operating system details
  - Complete dependency tree
  - Random seed impact assessment
  - Numerical precision considerations
  - Computational time documentation

### 1.4 Enhanced Statistical Reporting

#### Current Issues
- Focus on point estimates with basic confidence intervals
- Limited discussion of practical significance vs statistical significance
- Insufficient reporting of model diagnostics

#### Proposed Changes

**1.4.1 Comprehensive Model Diagnostics**
- For each model, report:
  - Residual analysis (for applicable models)
  - Cook's distance and influence diagnostics
  - Multicollinearity assessment (VIF)
  - Feature importance stability across folds
  - Learning curves (training vs validation error)
  - Calibration-in-the-large and calibration slope

**1.4.2 Effect Size and Practical Significance**
- Report effect sizes for all comparisons:
  - Absolute risk differences (not just ratios)
  - Number needed to evaluate (NNE)
  - Clinical/practical significance thresholds
  - Minimal detectable effect sizes
  - Equivalence testing (TOST) for fairness claims

**1.4.3 Publication-Standard Tables**
- Create formatted tables following criminology journal standards:
  - Table 1: Sample characteristics with standardized mean differences
  - Table 2: Model comparison with statistical tests
  - Table 3: Fairness metrics with confidence intervals and p-values
  - Table 4: Sensitivity analyses results
  - Appendix tables: Complete model outputs

---

## Part 2: Repository Reorganization for Interactive Analysis

### 2.1 Directory Structure Transformation

#### Current Structure
```
TabPFN-for-Criminology/
├── src/                    # Monolithic source code
├── scripts/                # Automated runner scripts
├── experiments/            # Experiment configurations
├── paper/                  # Manuscript
└── docs/                   # Documentation
```

#### Proposed Structure
```
TabPFN-for-Criminology/
├── notebooks/              # NEW: Interactive analysis notebooks
│   ├── 01_data_exploration/
│   │   ├── 01a_compas_eda.ipynb
│   │   ├── 01b_data_quality_assessment.ipynb
│   │   ├── 01c_missing_data_analysis.ipynb
│   │   └── 01d_descriptive_statistics.ipynb
│   ├── 02_preprocessing/
│   │   ├── 02a_data_cleaning.ipynb
│   │   ├── 02b_feature_engineering.ipynb
│   │   ├── 02c_train_test_split.ipynb
│   │   └── 02d_preprocessing_validation.ipynb
│   ├── 03_baseline_models/
│   │   ├── 03a_logistic_regression.ipynb
│   │   ├── 03b_tree_based_models.ipynb
│   │   ├── 03c_model_comparison.ipynb
│   │   └── 03d_hyperparameter_tuning.ipynb
│   ├── 04_tabpfn_experiments/
│   │   ├── 04a_tabpfn_zero_shot.ipynb
│   │   ├── 04b_tabpfn_finetuning.ipynb
│   │   ├── 04c_localpfn_retrieval.ipynb
│   │   └── 04d_tabpfn_comparison.ipynb
│   ├── 05_fairness_analysis/
│   │   ├── 05a_group_metrics.ipynb
│   │   ├── 05b_intersectional_fairness.ipynb
│   │   ├── 05c_fairness_interventions.ipynb
│   │   └── 05d_bias_auditing.ipynb
│   ├── 06_calibration_analysis/
│   │   ├── 06a_reliability_diagrams.ipynb
│   │   ├── 06b_calibration_metrics.ipynb
│   │   ├── 06c_recalibration_methods.ipynb
│   │   └── 06d_calibration_across_groups.ipynb
│   ├── 07_robustness_validation/
│   │   ├── 07a_temporal_validation.ipynb
│   │   ├── 07b_spatial_validation.ipynb
│   │   ├── 07c_sensitivity_analysis.ipynb
│   │   └── 07d_stability_assessment.ipynb
│   ├── 08_statistical_inference/
│   │   ├── 08a_hypothesis_testing.ipynb
│   │   ├── 08b_effect_sizes.ipynb
│   │   ├── 08c_power_analysis.ipynb
│   │   └── 08d_multiple_comparisons.ipynb
│   ├── 09_reporting/
│   │   ├── 09a_publication_tables.ipynb
│   │   ├── 09b_publication_figures.ipynb
│   │   ├── 09c_supplementary_materials.ipynb
│   │   └── 09d_results_summary.ipynb
│   └── 00_index.ipynb      # Master index with workflow overview
│
├── src/                    # Refactored as reusable library
│   ├── data/              # Data loading utilities only
│   ├── models/            # Model wrappers only
│   ├── evaluation/        # Metric functions only
│   ├── visualization/     # Plotting functions only
│   └── statistics/        # NEW: Statistical testing utilities
│
├── scripts/               # DEPRECATED: Keep for backwards compatibility
│   └── legacy/            # Move old scripts here
│
├── data/                  # NEW: Explicit data directory
│   ├── raw/              # Original downloaded datasets
│   ├── processed/        # Cleaned datasets
│   ├── interim/          # Intermediate processing steps
│   └── metadata/         # Data dictionaries, codebooks
│
├── results/              # NEW: All analysis outputs
│   ├── models/           # Saved model objects
│   ├── predictions/      # Model predictions
│   ├── metrics/          # Performance metrics
│   ├── figures/          # Generated plots
│   └── tables/           # Generated tables
│
├── docs/                 # Enhanced documentation
│   ├── methodology/      # NEW: Methodological documentation
│   ├── ethics/           # NEW: Ethical considerations
│   ├── data_cards/       # Enhanced data cards
│   └── guides/           # NEW: User guides
│
└── paper/                # Publication materials
    ├── manuscript/       # Main manuscript
    ├── supplements/      # Supplementary materials
    └── reviews/          # Review responses
```

### 2.2 Notebook Design Principles

#### 2.2.1 Modular Notebook Structure
Each notebook should:
- **Single Purpose:** Address one specific analytical step
- **Clear Narrative:** Mix code, visualizations, and markdown explanations
- **Reproducible:** Can be run independently with clear dependencies
- **Documented:** Extensive comments and explanations of choices
- **Checkpointed:** Save intermediate results for downstream notebooks

#### 2.2.2 Notebook Template Structure
Every notebook follows this structure:
```markdown
# Title: [Descriptive Title]

## Overview
- **Purpose:** What this notebook does
- **Inputs:** What data/artifacts are needed
- **Outputs:** What this notebook produces
- **Prerequisites:** Which notebooks should be run first

## Setup
- Import statements with explanations
- Configuration parameters
- Utility functions

## Analysis
- Step 1: [Description]
  - Code cells
  - Visualizations
  - Interpretations

- Step 2: [Description]
  - Code cells
  - Visualizations
  - Interpretations

## Results Summary
- Key findings from this notebook
- Decisions made and rationale
- Links to next steps

## Export
- Save artifacts for downstream analysis
- Document file formats and locations
```

#### 2.2.3 Interactive Elements
Each notebook includes:
- **Visualizations:** Every major step produces a plot
- **Summary Statistics:** Tables of key metrics
- **Diagnostic Checks:** Model diagnostics, data quality checks
- **Decision Points:** Explicit documentation of analytical choices
- **Alternative Paths:** Code for alternative approaches (commented out)

### 2.3 Source Code Refactoring

#### 2.3.1 Transform from Scripts to Library
Current scripts are monolithic. Refactor to:
- **Pure functions:** No side effects, testable
- **Minimal boilerplate:** Notebooks handle orchestration
- **Rich documentation:** Docstrings with examples
- **Type hints:** For clarity and IDE support

#### 2.3.2 New Statistical Utilities
Create `src/statistics/` module:
- `hypothesis_tests.py`: Statistical test functions
- `effect_sizes.py`: Effect size calculations
- `power_analysis.py`: Power and sample size functions
- `multiple_comparisons.py`: Correction methods
- `diagnostics.py`: Model diagnostic functions

#### 2.3.3 Enhanced Visualization Module
Expand `src/visualization/` with:
- `exploratory.py`: EDA plotting functions
- `diagnostic.py`: Model diagnostic plots
- `fairness.py`: Fairness visualization functions
- `calibration.py`: Calibration plot functions
- `publication.py`: Publication-quality figure formatting

### 2.4 Data Management Strategy

#### 2.4.1 Explicit Data Directory
Create clear data pipeline:
```
data/
├── raw/
│   ├── compas/
│   │   ├── compas-scores-two-years.csv
│   │   ├── README.md (provenance)
│   │   └── codebook.pdf
│   └── communities_crime/
│       ├── communities.data
│       ├── README.md
│       └── communities.names
│
├── processed/
│   ├── compas_cleaned.parquet
│   ├── compas_train.parquet
│   ├── compas_test.parquet
│   └── processing_log.json
│
├── interim/ (for multi-step preprocessing)
│   ├── compas_step1_filtered.parquet
│   └── compas_step2_encoded.parquet
│
└── metadata/
    ├── compas_data_dictionary.csv
    ├── variable_definitions.md
    └── data_versions.json
```

#### 2.4.2 Data Versioning
- Use parquet format for processed data (efficient, typed)
- Track data lineage with processing logs
- Version all datasets with hash checksums
- Document all transformations

### 2.5 Results Organization

#### 2.5.1 Structured Results Directory
```
results/
├── models/
│   ├── logistic_regression/
│   │   ├── model_fold_0.pkl
│   │   ├── hyperparameters.json
│   │   └── training_log.json
│   └── xgboost/
│       └── ...
│
├── predictions/
│   ├── compas_logistic_predictions.parquet
│   ├── compas_xgboost_predictions.parquet
│   └── prediction_metadata.json
│
├── metrics/
│   ├── performance_by_model.csv
│   ├── fairness_metrics.csv
│   ├── calibration_metrics.csv
│   └── metrics_metadata.json
│
├── figures/
│   ├── exploratory/
│   ├── model_performance/
│   ├── fairness/
│   ├── calibration/
│   └── publication_ready/ (high-res, styled)
│
└── tables/
    ├── table1_descriptive_stats.csv
    ├── table2_model_comparison.csv
    ├── table3_fairness_audit.csv
    └── tables_for_manuscript.xlsx
```

---

## Part 3: Implementation Plan

### Phase 1: Foundation (Week 1)

#### Day 1-2: Directory Restructuring
- [ ] Create new directory structure
- [ ] Move existing code to appropriate locations
- [ ] Set up data directories with README files
- [ ] Create results directory structure
- [ ] Update .gitignore for new structure

#### Day 3-4: Core Utilities Refactoring
- [ ] Refactor src/statistics/ module
- [ ] Refactor src/visualization/ module
- [ ] Create notebook utility functions
- [ ] Write comprehensive docstrings
- [ ] Add type hints throughout

#### Day 5-7: Methodological Documentation
- [ ] Write docs/methodology/analysis_plan.md
- [ ] Write docs/ethics/ethical_framework.md
- [ ] Write docs/methodology/theoretical_framework.md
- [ ] Expand data cards with detailed provenance
- [ ] Create research log template

### Phase 2: Core Notebooks (Week 2)

#### Day 8-9: Data Exploration Notebooks
- [ ] 01a_compas_eda.ipynb: Comprehensive EDA
- [ ] 01b_data_quality_assessment.ipynb: Missing data, outliers
- [ ] 01c_missing_data_analysis.ipynb: MCAR/MAR/MNAR analysis
- [ ] 01d_descriptive_statistics.ipynb: Publication Table 1

#### Day 10-11: Preprocessing Notebooks
- [ ] 02a_data_cleaning.ipynb: Filtering, validation
- [ ] 02b_feature_engineering.ipynb: Feature creation
- [ ] 02c_train_test_split.ipynb: Splitting strategy
- [ ] 02d_preprocessing_validation.ipynb: Verify splits

#### Day 12-14: Baseline Models Notebooks
- [ ] 03a_logistic_regression.ipynb: Full logistic analysis
- [ ] 03b_tree_based_models.ipynb: XGB, LGB, CB
- [ ] 03c_model_comparison.ipynb: Statistical comparisons
- [ ] 03d_hyperparameter_tuning.ipynb: Tuning exploration

### Phase 3: Advanced Analysis (Week 3)

#### Day 15-16: TabPFN Notebooks
- [ ] 04a_tabpfn_zero_shot.ipynb
- [ ] 04b_tabpfn_finetuning.ipynb
- [ ] 04c_localpfn_retrieval.ipynb
- [ ] 04d_tabpfn_comparison.ipynb

#### Day 17-18: Fairness Notebooks
- [ ] 05a_group_metrics.ipynb: By-group performance
- [ ] 05b_intersectional_fairness.ipynb: Intersectionality
- [ ] 05c_fairness_interventions.ipynb: Threshold optimization
- [ ] 05d_bias_auditing.ipynb: Comprehensive audit

#### Day 19-21: Calibration & Robustness
- [ ] 06a_reliability_diagrams.ipynb
- [ ] 06b_calibration_metrics.ipynb
- [ ] 06c_recalibration_methods.ipynb
- [ ] 06d_calibration_across_groups.ipynb
- [ ] 07a_temporal_validation.ipynb
- [ ] 07b_spatial_validation.ipynb
- [ ] 07c_sensitivity_analysis.ipynb
- [ ] 07d_stability_assessment.ipynb

### Phase 4: Statistical Inference & Reporting (Week 4)

#### Day 22-23: Statistical Notebooks
- [ ] 08a_hypothesis_testing.ipynb: McNemar, DeLong tests
- [ ] 08b_effect_sizes.ipynb: Cohen's d, NNE
- [ ] 08c_power_analysis.ipynb: Post-hoc power
- [ ] 08d_multiple_comparisons.ipynb: Bonferroni, Holm

#### Day 24-25: Reporting Notebooks
- [ ] 09a_publication_tables.ipynb: All manuscript tables
- [ ] 09b_publication_figures.ipynb: All manuscript figures
- [ ] 09c_supplementary_materials.ipynb: Appendices
- [ ] 09d_results_summary.ipynb: Executive summary

#### Day 26-28: Integration & Documentation
- [ ] 00_index.ipynb: Master notebook with workflow
- [ ] Update all documentation
- [ ] Write comprehensive README
- [ ] Create user guides
- [ ] Test full workflow end-to-end

---

## Part 4: Specific Enhancements for Criminology Methods Journal

### 4.1 Content Additions

#### 4.1.1 Methodological Innovations Section
Add to manuscript:
- Discussion of applying ML to criminology data
- Comparison to traditional criminological methods
- Best practices for validation in criminal justice contexts
- Guidelines for practitioners

#### 4.1.2 Limitations and Threats to Validity
Comprehensive discussion of:
- **Internal validity:** Selection bias, measurement error, confounding
- **External validity:** Generalizability across jurisdictions, time periods
- **Construct validity:** Do features measure intended constructs?
- **Statistical conclusion validity:** Power, violations of assumptions

#### 4.1.3 Ethical Considerations
In-depth treatment of:
- Historical injustices reflected in data
- Potential for algorithmic harm
- Stakeholder perspectives (defendants, judges, communities)
- Fairness as a contested concept
- Transparency vs privacy tradeoffs

### 4.2 Statistical Rigor Enhancements

#### 4.2.1 Pre-Registration
Create `docs/methodology/preregistration.md`:
- Primary and secondary hypotheses
- Analysis plan with decision rules
- Sample size justification
- Planned sensitivity analyses
- Criteria for exploratory vs confirmatory

#### 4.2.2 Multiverse Analysis
Implement systematic robustness checking:
- Document all researcher degrees of freedom
- Run analyses under multiple reasonable specifications
- Create specification curve analysis
- Report range of estimates across specifications

#### 4.2.3 Transparent Reporting
Follow reporting guidelines:
- TRIPOD+AI checklist for prediction models
- PROBAST for risk of bias assessment
- CONSORT-style flow diagram for sample selection
- Complete reporting of all analyses (not just "successful" ones)

### 4.3 Domain Integration

#### 4.3.1 Criminological Theory
Explicit connections to:
- Life-course criminology (age-crime curve)
- Social learning theory
- Strain theory
- Routine activities theory
- Developmental taxonomies (Moffitt, etc.)

#### 4.3.2 Policy Relevance
Discussion of:
- How models could inform decision-making
- What stakeholders need from risk assessment
- Implementation barriers
- Unintended consequences
- Monitoring and evaluation frameworks

---

## Part 5: Quality Assurance

### 5.1 Notebook Testing
- [ ] All notebooks run without errors
- [ ] Outputs are reproducible across runs
- [ ] Visualizations render correctly
- [ ] Intermediate files are created properly
- [ ] Dependencies are correctly specified

### 5.2 Documentation Review
- [ ] All functions have docstrings
- [ ] README is comprehensive and accurate
- [ ] User guides are clear and tested
- [ ] Methodological docs are complete
- [ ] Citations are accurate and complete

### 5.3 Code Quality
- [ ] Type hints throughout
- [ ] Consistent formatting (black, isort)
- [ ] No unused imports
- [ ] DRY principle applied
- [ ] Efficient data structures

### 5.4 Scientific Validity
- [ ] Statistical tests are appropriate
- [ ] Effect sizes reported
- [ ] Multiple comparisons handled
- [ ] Assumptions checked
- [ ] Sensitivity analyses conducted

---

## Part 6: Success Criteria

### 6.1 Usability
- [ ] A domain expert can run the full analysis
- [ ] Each notebook is self-contained and documented
- [ ] Clear workflow from raw data to results
- [ ] Intermediate results can be inspected easily
- [ ] Analytical choices are explicit and justified

### 6.2 Methodological Rigor
- [ ] All analyses pre-specified or marked exploratory
- [ ] Statistical power is adequate
- [ ] Effect sizes provide context
- [ ] Robustness checks are comprehensive
- [ ] Limitations are thoroughly discussed

### 6.3 Transparency
- [ ] All data transformations are documented
- [ ] Analytical decisions are logged
- [ ] Failed analyses are reported
- [ ] Code is readable and well-commented
- [ ] Results are fully reproducible

### 6.4 Domain Relevance
- [ ] Grounded in criminological theory
- [ ] Addresses practical concerns
- [ ] Considers ethical implications
- [ ] Provides actionable insights
- [ ] Suitable for criminology methods journal

---

## Part 7: Deliverables

### 7.1 Code
- [ ] 30+ interactive Jupyter notebooks
- [ ] Refactored Python modules as reusable library
- [ ] Comprehensive test suite
- [ ] CI/CD pipeline for testing

### 7.2 Documentation
- [ ] Comprehensive README with workflow guide
- [ ] Detailed methodological documentation
- [ ] Ethical framework document
- [ ] Theoretical framework document
- [ ] Complete data cards for all datasets
- [ ] User guides for each analysis phase

### 7.3 Outputs
- [ ] Publication-ready tables (Word/LaTeX)
- [ ] Publication-ready figures (high-res, vector)
- [ ] Supplementary materials
- [ ] Reproducibility package

### 7.4 Manuscript
- [ ] Methods section with full methodological detail
- [ ] Results section with comprehensive reporting
- [ ] Discussion emphasizing methodological contributions
- [ ] Limitations section addressing all threats to validity
- [ ] Appendices with full technical details

---

## Summary Timeline

| Phase | Duration | Focus |
|-------|----------|-------|
| Phase 1: Foundation | Week 1 (7 days) | Structure, utilities, documentation |
| Phase 2: Core Notebooks | Week 2 (7 days) | EDA, preprocessing, baselines |
| Phase 3: Advanced Analysis | Week 3 (7 days) | TabPFN, fairness, calibration |
| Phase 4: Inference & Reporting | Week 4 (7 days) | Statistics, publication materials |
| **Total** | **28 days** | **Complete transformation** |

---

## Next Steps

1. **User Review:** Review this workplan and approve/modify
2. **Prioritization:** Identify must-have vs nice-to-have components
3. **Sequencing:** Confirm implementation order
4. **Begin Implementation:** Start with Phase 1, Day 1

---

**This workplan transforms the repository from an automated ML pipeline to an interactive, methodologically rigorous criminology research package suitable for publication in top criminology methods journals.**
