# Editorial Review: TabPFN for Criminology Study

**Reviewer Role:** Senior Professor in Criminology & Data Science, Editorial Board Member

**Date:** 2025-11-19

**Overall Assessment:** Major Revisions Required

---

## Executive Summary

This manuscript presents a methodologically rigorous framework for evaluating TabPFN (a tabular foundation model) on criminal justice prediction tasks. The work demonstrates **exceptional technical sophistication** in ML methodology, statistical rigor, and fairness analysis. However, for publication in **top criminology journals**, the study requires substantial reorientation from a machine learning benchmark paper to a criminologically-grounded empirical investigation.

**Current Fit:**
- ✅ **Strong fit:** Computational social science methods journals (e.g., *Sociological Methods & Research*, *Political Analysis*)
- ⚠️ **Possible fit with revisions:** *Journal of Quantitative Criminology*, *Justice Quarterly*
- ❌ **Poor fit without major reframing:** *Criminology*, *Journal of Research in Crime and Delinquency*

---

## Major Strengths (Continue These)

### 1. **Methodological Rigor** ⭐⭐⭐⭐⭐
- Pre-registered analysis plan (rare in criminology)
- Proper statistical hypothesis testing (DeLong, McNemar's) with multiple comparison corrections
- Effect sizes and confidence intervals reported
- Comprehensive documentation of analytical decisions
- **This is exceptional and should be a model for the field**

### 2. **Ethical Framework** ⭐⭐⭐⭐⭐
- The 800-line ethical framework is **outstanding**
- Thoughtful engagement with stakeholder impacts
- Acknowledgment of historical biases in criminal justice data
- Clear discussion of error cost asymmetry (FP vs FN)
- **This alone could be published as a standalone methods paper**

### 3. **Fairness Analysis** ⭐⭐⭐⭐⭐
- Proper acknowledgment of impossibility theorems (Kleinberg et al., Chouldechova)
- Intersectional analysis (race × gender × age)
- Multiple fairness criteria evaluated
- Transparent reporting of trade-offs
- **Excellent integration of fairness ML literature with criminology context**

### 4. **Critical Evaluation** ⭐⭐⭐⭐
- Balanced assessment of TabPFN limitations (not advocacy)
- Explicit "NOT recommended for deployment" statements
- Discussion of accountability and interpretability barriers
- **Refreshingly honest compared to typical ML papers**

### 5. **Reproducibility** ⭐⭐⭐⭐⭐
- Well-structured notebooks with clear documentation
- Statistical utilities properly implemented
- Code appears professionally written
- **Sets a high standard for open science**

---

## Critical Weaknesses (Must Address)

### 1. **CRIMINOLOGICAL THEORY: MISSING** ⚠️⚠️⚠️

**Problem:** This reads like a computer science paper applied to criminal justice data, not a criminology paper.

**What's Missing:**
- **No theoretical framework** for why we're predicting recidivism
- **No engagement** with criminological theories (e.g., life-course theory, labeling theory, strain theory, desistance literature)
- **No discussion** of what "recidivism" means substantively (vs. technically)
- **No consideration** of whether prediction itself is compatible with rehabilitation goals

**What Reviewers Will Ask:**
- "Why should criminologists care about a 0.01 improvement in AUROC?"
- "What does this tell us about crime causation or criminal justice policy?"
- "How does this advance criminological knowledge beyond existing risk assessment literature?"

**Recommendations:**
1. **Add theoretical section** grounding recidivism prediction in criminology
   - Discuss life-course perspectives (Sampson & Laub, Moffitt)
   - Engage with desistance literature (Maruna, Laub & Sampson)
   - Address labeling theory concerns (Becker) - does prediction create labels?

2. **Reframe research questions** in substantive terms:
   - Instead of: "Does fine-tuning improve AUROC?"
   - Try: "Can foundation models capture complex, non-linear pathways to recidivism identified in life-course theory?"

3. **Interpret results through criminological lens:**
   - What do model failures tell us about limits of prediction?
   - Which types of individuals are hardest to predict and why?
   - Do models capture known criminological risk factors (e.g., age-crime curve)?

### 2. **SUBSTANTIVE CONTRIBUTION: UNCLEAR** ⚠️⚠️⚠️

**Problem:** The study is primarily a **methods comparison** (TabPFN vs. baselines), not a substantive investigation of crime or criminal justice.

**Current Results Show:**
- **No significant differences** between models (all p > 0.05 after correction)
- AUROC ≈ 0.71 for all models (consistent with prior literature)
- Logistic regression performs best (simplest model wins)
- **TabPFN fine-tuning not completed** (missing the main contribution!)

**What This Means:**
- The "novel" method (TabPFN) doesn't outperform 1990s technology (logistic regression)
- The answer to RQ1 appears to be "No, domain adaptation does not improve performance"
- **This is actually an important finding!** But needs to be framed correctly

**Recommendations:**
1. **Reframe as a "negative result" paper:**
   - Title: "Why Foundation Models Fail at Recidivism Prediction: Lessons for Algorithmic Criminal Justice"
   - Emphasize that **simpler is better** for high-stakes decisions
   - Argue for interpretability over marginal performance gains

2. **Add substantive analysis:**
   - Which criminological risk factors matter most? (Feature importance)
   - Do models capture age-crime curve, prior record effects?
   - Error analysis: Who gets misclassified and why?
   - Case studies: Qualitative examination of false positives/negatives

3. **Policy implications:**
   - If logistic regression is sufficient, jurisdictions should use it (interpretable, cheaper)
   - Black-box models (TabPFN) offer no practical advantage
   - Fairness gaps persist regardless of model choice → systemic problem, not technical

### 3. **LITERATURE REVIEW: TOO ML-FOCUSED** ⚠️⚠️

**Problem:** Heavy on machine learning conferences (ICLR, NeurIPS, FAccT), light on criminology journals.

**Missing Criminology Literature:**
- **Risk assessment:** Bonta & Andrews, Gottfredson & Moriarty, Baird et al.
- **COMPAS critiques:** Dressel & Farid (Science Advances), Corbett-Davies et al., Rudin et al.
- **Recidivism research:** Gendreau et al., Langan & Levin (BJS reports)
- **Algorithmic fairness in CJ:** Mayson, Starr, Skeem & Lowenkamp
- **Practitioner perspectives:** Literature on judicial use of risk assessments

**Recommendations:**
1. Expand literature review to ~40% criminology, 40% methods, 20% ML
2. Engage with **skeptical** criminology literature on risk assessment
3. Cite **Bureau of Justice Statistics** reports (this is the gold standard for criminal justice data)
4. Reference **legal scholarship** on algorithmic sentencing

### 4. **DATA SCOPE: TOO NARROW** ⚠️⚠️

**Problem:** Only COMPAS data analyzed (n=5,000). Three other datasets mentioned but not used.

**Limitations:**
- **Single county** (Broward, FL) - limited generalizability
- **2013-2014** data - nearly a decade old
- **No temporal validation** - can't assess model degradation
- **No geographic variation** - COMPAS is unique to Florida

**What Reviewers Will Say:**
- "Findings may not generalize beyond Broward County"
- "Need multi-site validation"
- "Where are the other datasets mentioned in the manuscript?"

**Recommendations:**
1. **Be honest** that this is a proof-of-concept on one dataset
2. **Add temporal analysis:**
   - Train on 2013, test on 2014
   - Show whether models degrade over time
   - Discuss concept drift

3. **Future work:** Clearly state that replication on NIJ Recidivism Forecasting Challenge data is needed

4. **Alternatively:** Drop claims about "Communities & Crime, NCVS, UCR" unless you analyze them

### 5. **RESULTS PRESENTATION: INCOMPLETE** ⚠️⚠️

**Problem:** The manuscript draft has empty tables and placeholder text.

**Missing:**
- TabPFN fine-tuned results (the main RQ!)
- LocalPFN results
- Temporal validation results
- Spatial validation results
- Calibration analysis results
- Complete fairness results

**What This Means:**
- **Study appears unfinished**
- Can't evaluate primary hypotheses
- Effect sizes not fully reported

**Recommendations:**
1. **Complete all analyses** before claiming "publication-ready"
2. **Run TabPFN fine-tuning** or acknowledge it's not feasible
3. **If fine-tuning fails**, frame as limitation and focus on zero-shot vs. baselines
4. **Populate all tables** with actual results
5. **Add robustness checks** (cross-validation, bootstrap, sensitivity analyses)

### 6. **POLICY RELEVANCE: UNDERDEVELOPED** ⚠️⚠️

**Problem:** Extensive disclaimers about "research only, not deployment," but limited constructive guidance for practitioners.

**What's Missing:**
- **Actionable recommendations** for jurisdictions using risk assessment
- **Comparison to existing tools** (COMPAS, LSI-R, ORAS, PSA)
- **Cost-benefit analysis** - is ML worth the complexity?
- **Implementation considerations** - what would practitioners need to know?

**Recommendations:**
1. **Add "Implications for Practice" section:**
   - If logistic regression is sufficient, recommend simpler tools
   - Provide guidance on threshold selection for different policy goals
   - Discuss how to monitor fairness post-deployment

2. **Engage with existing risk tools:**
   - How does your logistic regression compare to COMPAS, LSI-R?
   - What features matter most? (practitioners care about this)
   - Can you build a simpler, transparent tool that performs as well?

3. **Cost-benefit framing:**
   - TabPFN requires GPU, technical expertise, ongoing maintenance
   - Logistic regression can run on a calculator
   - For 0.01 AUROC gain, complexity not justified

### 7. **FRAMING: OVERSELLING** ⚠️

**Problem:** Language suggests this is ready for top journals, but work is incomplete and contributions unclear.

**Examples of Overselling:**
- "Publication-ready framework" (but results incomplete)
- "Suitable for top criminology journals" (but lacks criminology theory)
- "Comprehensive evaluation" (but only one dataset analyzed)
- "22 notebooks" (true, but quantity ≠ quality)

**Recommendations:**
1. **Be modest:** This is a solid working paper, not yet ready for *Criminology*
2. **Acknowledge limitations** prominently in abstract
3. **Frame as methodological contribution** to computational criminology
4. **Target realistic venues** initially:
   - *Journal of Quantitative Criminology* (methods-focused)
   - *Journal of Experimental Criminology* (if you add causal framing)
   - *Crime and Delinquency* (more receptive to methods papers)

---

## Specific Suggestions for Top Journals

### For *Journal of Quantitative Criminology*:

**What They Want:**
- Methodological innovation with criminological application
- Rigorous statistical analysis (you have this!)
- Comparison to existing methods
- Practical utility for researchers

**How to Revise:**
1. **Title:** "Evaluating Tabular Foundation Models vs. Traditional Methods for Recidivism Prediction: A Methodological Comparison"
2. **Reframe** as methods paper, not applied paper
3. **Add simulation study** showing when TabPFN might be useful (small samples, many features, non-linear effects)
4. **Compare to published COMPAS results** from ProPublica, Dressel & Farid
5. **Provide software package** for criminologists to use (R or Python)

### For *Criminology* (Top Tier - Major Revisions Needed):

**What They Want:**
- Advances criminological theory
- Substantive findings about crime/justice
- Policy relevance
- Accessible to non-quantitative readers

**How to Revise:**
1. **Completely reframe:**
   - Title: "The Limits of Prediction: What Machine Learning Reveals About the Complexity of Desistance"
   - Focus on **what we can't predict** (failures are theoretically interesting!)
   - Tie errors to life-course theory (turning points, agency, redemption scripts)

2. **Add qualitative component:**
   - Case studies of misclassified individuals
   - Interviews with probation officers about how they use risk scores
   - Discussion of harm from false positives (real human costs)

3. **Theoretical contribution:**
   - Argue that prediction has fundamental limits due to human agency
   - Models capture static factors (prior record) but miss dynamic factors (motivation to desist)
   - Connect to Maruna's desistance narratives, Laub & Sampson's turning points

4. **Cut technical jargon:**
   - Non-specialists don't care about "DeLong tests" or "Holm-Bonferroni correction"
   - Move technical details to appendix
   - Focus on substantive interpretation

### For *Justice Quarterly*:

**What They Want:**
- Criminal justice policy focus
- Practitioner relevance
- Empirical rigor
- Fairness and equity

**How to Revise:**
1. **Title:** "Algorithmic Risk Assessment in Practice: Comparing Foundation Models to Traditional Approaches in Recidivism Prediction"

2. **Add practitioner survey:**
   - How do judges/probation officers currently use risk scores?
   - What barriers to adoption exist?
   - What interpretability do they need?

3. **Policy analysis:**
   - Review state legislation on algorithmic tools
   - Discuss legal requirements (right to explanation)
   - Provide implementation checklist

4. **Fairness as central theme:**
   - Emphasize impossibility theorems (cannot satisfy all criteria)
   - Discuss how practitioners should navigate trade-offs
   - Recommend stakeholder engagement processes

---

## Minor Issues (Easily Fixed)

### Writing & Presentation:

1. **Abstract:** Too technical. Needs 1-2 sentences on "why criminologists should care"

2. **Introduction:** Should start with a criminology question, not ML methods
   - Current: "Foundation models offer promise..."
   - Better: "Recidivism prediction has long challenged criminologists. Despite decades of research..."

3. **Jargon:** Assume readers unfamiliar with "transformers," "in-context learning," "Pareto frontiers"
   - Add glossary or explain terms on first use
   - Or move technical details to methods appendix

4. **Figures:** Need better captions explaining substantive interpretation
   - Current: "ROC curves for all models"
   - Better: "Predictive accuracy remains modest across all approaches (AUROC ≈ 0.71), suggesting fundamental limits to prediction"

5. **Tables:** Too many numbers, not enough interpretation
   - Add "What This Means" column for each table
   - Highlight substantively important differences (not just statistical significance)

### Citations:

1. **Add classic criminology:**
   - Wolfgang, Figlio, & Sellin (1972) - *Delinquency in a Birth Cohort*
   - Hirschi (1969) - *Causes of Delinquency*
   - Sampson & Laub (1993) - *Crime in the Making*

2. **Add BJS reports:**
   - "Recidivism of Prisoners Released in 30 States" (Durose et al.)
   - "Recidivism of Federal Offenders" (Hunt & Dumville)

3. **Add legal scholarship:**
   - Mayson (2018) - "Bias In, Bias Out" (Yale Law Journal)
   - Starr (2014) - "Evidence-Based Sentencing and the Scientific Rationalization of Discrimination"

4. **Add criminology journals:**
   - Too many arXiv preprints, too few peer-reviewed criminology papers

### Data & Methods:

1. **Data card:** Excellent idea, but add:
   - Comparison to national recidivism rates (is COMPAS representative?)
   - Discussion of why ProPublica's sample may be biased
   - Limitations of arrest-based recidivism (detection bias)

2. **Missing data analysis:** You mention it but don't show results
   - What % missing for each variable?
   - Sensitivity to imputation methods?

3. **Feature engineering:**
   - Why these 14 features?
   - Did you consider interactions (age × prior record)?
   - What about non-linear transformations?

4. **Calibration:** Mentioned but no results shown
   - Reliability diagrams?
   - ECE values?
   - Clinical implications of miscalibration?

---

## Recommendations by Priority

### MUST DO (Before Submission):

1. ✅ **Complete all analyses** (TabPFN fine-tuning, all datasets, or remove claims)
2. ✅ **Add criminological theory** section (20-30% of paper)
3. ✅ **Reframe research questions** in substantive terms
4. ✅ **Expand literature review** to include criminology journals
5. ✅ **Add substantive interpretation** of results (feature importance, error analysis)
6. ✅ **Populate all tables** with actual results
7. ✅ **Decide on target journal** and tailor framing accordingly

### SHOULD DO (Strengthen Manuscript):

8. ⚡ **Add temporal validation** (train on 2013, test on 2014)
9. ⚡ **Add case studies** of misclassified individuals
10. ⚡ **Compare to existing tools** (COMPAS scores, LSI-R)
11. ⚡ **Simplify language** for non-technical readers
12. ⚡ **Add policy recommendations** section
13. ⚡ **Discuss cost-benefit** of complex models vs. simple ones

### NICE TO HAVE (Strengthen Further):

14. 💡 **Practitioner interviews** or survey
15. 💡 **Qualitative analysis** of errors
16. 💡 **Simulation study** showing when TabPFN might excel
17. 💡 **Software package** for criminologists
18. 💡 **Replication on additional datasets**

---

## Suggested Reframing (Example)

### Current Framing (ML-focused):
> "We evaluate TabPFN variants (zero-shot, fine-tuned, and LocalPFN with retrieval+fine-tuning) against well-tuned baselines on four criminology datasets..."

### Suggested Reframing (Criminology-focused):
> "Recidivism prediction has long challenged criminologists, with decades of research identifying risk factors yet achieving only modest predictive accuracy (AUROC ≈ 0.70). Recent advances in machine learning—particularly foundation models pre-trained on large corpora—promise to capture complex, non-linear patterns that traditional methods might miss. We test this promise by comparing a state-of-the-art foundation model (TabPFN) to traditional approaches on a widely-studied dataset (COMPAS). Results suggest that **complexity offers no advantage**: simple logistic regression matches or exceeds foundation model performance, while offering superior interpretability. We discuss implications for algorithmic risk assessment policy, arguing that jurisdictions should prioritize transparency over marginal predictive gains."

**See the difference?**
- Starts with criminology question
- Contextualizes ML as tool, not focus
- Emphasizes substantive finding (simple is better)
- Ends with policy implications

---

## Honest Assessment

### What Reviewers Will Like:
- ⭐ Methodological rigor (rare in criminology)
- ⭐ Fairness analysis (timely and important)
- ⭐ Ethical framework (thoughtful and comprehensive)
- ⭐ Reproducibility (open code, data, documentation)
- ⭐ Honesty about limitations (refreshing)

### What Reviewers Will Criticize:
- ❌ Lack of criminological theory
- ❌ Unclear substantive contribution
- ❌ Limited data (one county, one time period)
- ❌ Results incomplete (missing primary analyses)
- ❌ Overselling (claims not supported by results)
- ❌ Too technical for general criminology audience

### Bottom Line:

**This is excellent work** that demonstrates rare methodological sophistication. However, it's **not yet ready for top criminology journals** without substantial revision. The work is caught between two audiences:

1. **Machine learning researchers** (who want novel methods and benchmark datasets)
2. **Criminologists** (who want theoretical insights and policy relevance)

**My recommendation:** Choose your audience and revise accordingly.

**Option A - Methods Journal (Easier Path):**
- Target: *Journal of Quantitative Criminology*, *Sociological Methods & Research*
- Frame as methodological contribution
- Emphasize statistical rigor, reproducibility
- Less theory needed, more technical detail acceptable
- **Timeline: 3-6 months of revisions**

**Option B - Substantive Journal (Harder but Higher Impact):**
- Target: *Criminology*, *Justice Quarterly*
- Complete reframe around criminology theory
- Add qualitative component (case studies, interviews)
- Simplify technical presentation
- Emphasize "simpler is better" finding
- **Timeline: 6-12 months of additional work**

**My honest advice:** Go with **Option A first**. Publish this as a methods paper in JQC (which is highly respected). Then, if you want to reach *Criminology*, do a follow-up study that:
- Replicates on multiple datasets
- Adds qualitative depth
- Connects failures to theory
- Engages practitioners

**This is a publishable paper, but know your audience and set realistic expectations.**

---

## Final Thoughts

You've built something genuinely valuable:
- A reproducible framework for ML in criminology
- An ethical template for high-stakes prediction
- A demonstration that rigor is possible in this space

**Don't let perfect be the enemy of good.** Publish this as a methods contribution, get feedback, iterate. The criminology field needs more work like this—just frame it appropriately.

**I would be happy to see this in JQC with appropriate revisions.**

Good luck!

---

**Recommended Next Steps:**
1. Read 5-10 recent papers in your target journal
2. Identify which framing fits your goals
3. Complete missing analyses
4. Draft "criminology theory" section
5. Get feedback from criminology colleagues (not just ML folks)
6. Revise and resubmit with realistic framing

**Estimated Effort:**
- Option A (Methods journal): ~100-150 hours
- Option B (Top substantive journal): ~300-500 hours

Choose wisely!
