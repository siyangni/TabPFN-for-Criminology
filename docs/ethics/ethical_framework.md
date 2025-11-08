# Ethical Framework: TabPFN for Criminology Research

**Project:** Optimizing Tabular Foundation Models for Criminology

**Version:** 1.0

**Date:** 2025-11-08

**Status:** Living Document (Updated as ethical considerations evolve)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Ethical Principles](#2-ethical-principles)
3. [Stakeholder Impact Analysis](#3-stakeholder-impact-analysis)
4. [Historical Context and Bias](#4-historical-context-and-bias)
5. [Error Cost Asymmetry](#5-error-cost-asymmetry)
6. [Fairness as a Contested Concept](#6-fairness-as-a-contested-concept)
7. [Potential for Harm](#7-potential-for-harm)
8. [Mitigation Strategies](#8-mitigation-strategies)
9. [Limitations and Transparency](#9-limitations-and-transparency)
10. [Responsible Deployment](#10-responsible-deployment)
11. [Community Engagement](#11-community-engagement)
12. [Ongoing Ethical Review](#12-ongoing-ethical-review)

---

## 1. Executive Summary

This document outlines the ethical framework guiding our research on applying TabPFN to criminology prediction tasks. Criminal justice prediction is a **high-stakes domain** where algorithmic errors have profound consequences for individuals, families, and communities.

**Core Ethical Commitments:**

1. **Do No Harm:** Minimize potential for algorithmic harm while advancing scientific knowledge
2. **Transparency:** Fully disclose methods, limitations, and potential biases
3. **Fairness:** Explicitly evaluate and report disparate impacts across demographic groups
4. **Accountability:** Take responsibility for how research may be used
5. **Justice:** Consider impacts on historically marginalized communities

**Research Scope:**
- **What we ARE doing:** Evaluating TabPFN as a benchmark against baselines, with comprehensive fairness auditing
- **What we are NOT doing:** Recommending deployment, making causal claims, or advocating for specific policies

---

## 2. Ethical Principles

### 2.1 Guiding Frameworks

Our research adheres to established ethical frameworks:

**Belmont Report Principles:**
1. **Respect for Persons:** Recognize dignity and autonomy of individuals in datasets
2. **Beneficence:** Maximize benefits, minimize harms
3. **Justice:** Fair distribution of research benefits and burdens

**ACM Code of Ethics:**
1. Contribute to society and human well-being
2. Avoid harm
3. Be honest and trustworthy
4. Be fair and take action not to discriminate
5. Respect privacy

**Fairness, Accountability, and Transparency (FAT/FAccT) Principles:**
- Interrogate systems for bias
- Consider social context
- Involve affected communities
- Enable contestability

### 2.2 Domain-Specific Considerations

Criminal justice prediction raises unique ethical issues:

**Power Imbalances:**
- Subjects of prediction have limited agency
- Predictions can become self-fulfilling
- Errors disproportionately harm the powerless

**Historical Injustice:**
- Criminal justice data reflects centuries of discrimination
- "Ground truth" labels (arrests, convictions) are socially constructed
- Algorithms risk perpetuating historical injustices

**Procedural Justice:**
- Affected individuals should understand how decisions are made
- Predictions should be contestable
- Human oversight is essential

---

## 3. Stakeholder Impact Analysis

### 3.1 Identified Stakeholders

We identify and consider impacts on multiple stakeholder groups:

#### **Primary Stakeholders** (Directly affected by predictions)

**1. Defendants/Individuals Being Assessed**
- **Potential Benefits:** More accurate risk assessment may lead to fairer decisions
- **Potential Harms:**
  - False positives → Unwarranted detention, loss of liberty
  - Stigmatization from high-risk labels
  - Reduced agency in decision-making
  - Privacy violations from data collection
- **Specific Concerns:**
  - Members of historically discriminated groups (Black defendants, women, youth)
  - First-time offenders vs repeat offenders
  - Those with mental health or substance abuse issues

**2. Families and Communities**
- **Potential Benefits:** Reduced incarceration may keep families intact
- **Potential Harms:**
  - False negatives → Public safety concerns if high-risk individuals released
  - Community-level impacts of concentrated surveillance
  - Intergenerational trauma from over-policing
- **Specific Concerns:**
  - Communities of color disproportionately affected
  - Children of incarcerated parents
  - Economic impacts on families

#### **Secondary Stakeholders** (Use predictions to make decisions)

**3. Judges and Court Personnel**
- **Potential Benefits:** Additional information for decision-making
- **Potential Harms:**
  - Over-reliance on algorithmic predictions ("automation bias")
  - Abdication of judicial discretion
  - Deskilling of risk assessment expertise
- **Specific Concerns:**
  - Judges in under-resourced courts
  - Variability in algorithmic literacy

**4. Probation Officers and Correctional Staff**
- **Potential Benefits:** Risk-needs assessment for resource allocation
- **Potential Harms:**
  - Increased surveillance of high-risk individuals
  - Reduced therapeutic relationships
  - Liability concerns if predictions wrong
- **Specific Concerns:**
  - Officers with large caseloads
  - Competing organizational incentives

**5. Prosecutors and Defense Attorneys**
- **Potential Benefits:** Evidence for plea negotiations, sentencing arguments
- **Potential Harms:**
  - Unequal access to algorithmic challenges (well-resourced vs public defenders)
  - Pressure to accept algorithmic predictions
- **Specific Concerns:**
  - Indigent defendants with minimal legal representation

#### **Tertiary Stakeholders** (Broader societal interests)

**6. Policy Makers and Legislators**
- **Interests:** Evidence-based policy, cost savings, public safety, equity
- **Risks:** Misinterpreting research, implementing without safeguards

**7. Researchers and Academics**
- **Interests:** Scientific advancement, reproducibility, ethical research
- **Risks:** Ivory tower disconnect from real-world impacts

**8. General Public**
- **Interests:** Public safety, fairness, efficient use of resources
- **Risks:** Misinformation, fear-driven policy, erosion of civil liberties

**9. Vendors and Technology Companies**
- **Interests:** Commercial deployment, market expansion
- **Risks:** Profit motive overriding fairness, proprietary opacity

### 3.2 Stakeholder Engagement Plan

**Minimal Engagement (Research Stage):**
- Literature review of affected community perspectives
- Consultation with criminal justice reform organizations
- Review of court challenges to algorithmic risk assessment

**Recommended Engagement (Before Deployment):**
- Focus groups with formerly incarcerated individuals
- Surveys of judges, probation officers, defense attorneys
- Community review boards in affected neighborhoods
- Co-design with stakeholders at all stages

**Note:** Our research does NOT involve deployment; engagement is aspirational for future work.

---

## 4. Historical Context and Bias

### 4.1 Historical Injustices in Criminal Justice

**Context is Critical:**

The criminal justice system in the United States has a documented history of racial discrimination:

1. **Slavery and Black Codes:** Origins of racialized social control
2. **Jim Crow Laws:** Legal segregation and criminalization of Black life
3. **War on Drugs:** Disproportionate incarceration of Black and Latino communities
4. **Mass Incarceration:** U.S. incarceration rate 5-10x other democracies
5. **Differential Policing:** Over-policing in communities of color, under-policing of white-collar crime

**Data Reflects This History:**
- Arrest rates reflect policing patterns, not just criminal behavior
- Conviction rates reflect prosecutorial discretion and plea bargaining
- Sentencing reflects judicial bias (documented in lab and field studies)
- Recidivism labels reflect surveillance intensity (more surveillance = more detection)

### 4.2 Construct Validity of "Recidivism"

**Recidivism is NOT a neutral outcome:**

- **Measured as:** Re-arrest, re-conviction, or re-incarceration
- **Depends on:** Surveillance intensity, police presence, prosecutorial decisions
- **Varies by:** Geography, race, socioeconomic status
- **Examples:**
  - Two individuals commit same offense → One in heavily-policed area arrested, one not
  - Two individuals arrested → One with public defender pleads guilty, one with private attorney gets charges dropped

**Implications:**
- Labels are "proxy labels" not "ground truth"
- Models trained on these labels inherit biases
- High accuracy ≠ fairness or justice

### 4.3 Acknowledging Structural Inequity

**Our Research Position:**

We acknowledge that:
1. **Data is biased:** Reflects historical and ongoing discrimination
2. **"Objective" prediction is impossible:** Bias is in the data-generating process
3. **Optimization may worsen bias:** Maximizing accuracy on biased labels can amplify disparities
4. **We are complicit:** Even benchmark research legitimizes predictive tools

**Our Response:**
- Explicit fairness auditing across demographic groups
- Intersectional analysis (race × sex, race × age)
- Qualitative discussion of structural inequity
- No claims of "bias-free" or "objective" prediction
- Clear limitations on use of findings

---

## 5. Error Cost Asymmetry

### 5.1 Error Types and Consequences

**Confusion Matrix for Recidivism Prediction:**

|               | Predicted: Will Recidivate | Predicted: Will Not Recidivate |
|---------------|---------------------------|-------------------------------|
| **Actually Recidivates** | True Positive (TP) | False Negative (FN) |
| **Does Not Recidivate** | False Positive (FP) | True Negative (TN) |

### 5.2 Differential Impacts by Error Type

#### **False Positives (Predicted to recidivate, actually won't)**

**Consequences for Individual:**
- Denied pre-trial release → Jail time for innocent until proven guilty
- Harsher sentence → Years of lost liberty
- Denied parole → Extended incarceration
- Denied rehabilitation programs → Reduced opportunities
- Stigmatization → Psychological harm, damaged relationships
- Economic harm → Job loss, housing loss, family strain

**Societal Costs:**
- Incarceration costs: ~$35,000/year per person
- Lost productivity and wages
- Family disruption, children in foster care
- Community-level trauma

**Equity Concern:** ProPublica found Black defendants twice as likely to be false positives as White defendants (45% vs 23%)

#### **False Negatives (Predicted not to recidivate, actually will)**

**Consequences:**
- Public safety risk if released
- Victims harmed by preventable crimes
- Political backlash, reduced support for reform
- Erosion of public trust in risk assessment

**Societal Costs:**
- Victimization costs (physical, psychological, economic)
- Law enforcement and court costs
- Political costs to reform efforts

**Equity Concern:** ProPublica found White defendants more likely to be false negatives than Black defendants (48% vs 28%)

### 5.3 Error Cost Analysis

**Traditional ML assumes equal error costs:**
- Minimize overall error rate
- Treat FP and FN as equivalent

**Reality in criminal justice:**
- FP: Wrongful detention (liberty loss)
- FN: Public safety risk (potential victimization)

**Ethical Questions:**
1. Is one year of wrongful detention equivalent to one prevented crime?
2. Who decides the relative costs?
3. How do we account for base rates? (If 30% recidivate, any detained individual has 70% chance of FP)

**Our Approach:**
- Report FP and FN rates separately, not just overall accuracy
- Report error rates by demographic group
- Discuss threshold selection as value judgment
- NO recommendation on "optimal" threshold (this requires stakeholder input)
- Fairness-accuracy tradeoff curves to visualize choices

### 5.4 Stakeholder-Specific Error Costs

| Stakeholder | Prefers Low FP | Prefers Low FN |
|-------------|---------------|----------------|
| Defendants | ✓ (avoid wrongful detention) | |
| Public/Victims | | ✓ (avoid victimization) |
| Prosecutors | | ✓ (political pressure) |
| Defense Attorneys | ✓ (client interest) | |
| Judges | Balanced (judicial discretion) | Balanced |
| Reform Advocates | ✓ (reduce incarceration) | |
| Law Enforcement | | ✓ (public safety mission) |

**Implication:** No single error rate satisfies all stakeholders → Requires deliberation and compromise.

---

## 6. Fairness as a Contested Concept

### 6.1 Multiple Fairness Definitions

**Mathematical fairness metrics are incompatible:**

1. **Demographic Parity:** P(Ŷ=1 | A=a) = P(Ŷ=1 | A=b)
   - Equal positive prediction rates across groups
   - Ignores differential base rates
   - May require different accuracy across groups

2. **Equalized Odds:** P(Ŷ=1 | Y=y, A=a) = P(Ŷ=1 | Y=y, A=b)
   - Equal TPR and FPR across groups
   - Allows different positive prediction rates
   - May be impossible if base rates differ (Chouldechova, 2017; Kleinberg et al., 2017)

3. **Predictive Parity:** P(Y=1 | Ŷ=1, A=a) = P(Y=1 | Ŷ=1, A=b)
   - Equal PPV across groups (predicted positive → actually positive)
   - May require different FPR across groups
   - Incompatible with equalized odds when base rates differ

4. **Individual Fairness:** Similar individuals should receive similar predictions
   - Requires defining "similarity" (circular problem)
   - May be satisfied while group fairness violated

5. **Counterfactual Fairness:** Prediction wouldn't change if individual's race/sex changed
   - Requires causal model (strong assumptions)
   - May be impossible if race affects outcomes through legitimate pathways

**Impossibility Theorems:**
- Cannot satisfy calibration, equalized odds, AND demographic parity simultaneously when base rates differ (Chouldechova, 2017; Kleinberg et al., 2017)
- Tradeoffs are unavoidable

### 6.2 Our Fairness Approach

**Embrace Pluralism:**

We reject the notion of a single "fair" metric. Instead:

1. **Report Multiple Metrics:** Demographic parity, equalized odds, predictive parity, group-specific metrics
2. **Visualize Tradeoffs:** Fairness-accuracy Pareto frontiers
3. **Transparent Limitations:** Explicitly state which fairness criteria are violated
4. **No False Claims:** We will NOT claim "fairness" without qualification
5. **Defer to Stakeholders:** Metric choice should involve affected communities, not just researchers

**Primary Metrics (with rationale):**
- **Equalized Odds:** Widely used, interpretable, connects to procedural justice
- **Demographic Parity:** Simple, addresses disparate impact doctrine
- **Group-Specific TPR/FPR:** Transparent, allows stakeholders to assess impacts

**Secondary Metrics:**
- **Predictive parity:** Relevant for decision-makers
- **Fairness ratios:** Quantifies relative disparities

### 6.3 Philosophical Perspectives on Fairness

**Different ethical frameworks prioritize different fairness concepts:**

**Consequentialism/Utilitarianism:**
- Maximize overall welfare
- May sacrifice individual fairness for aggregate outcomes
- Tension: Should we optimize for public safety (FN minimization) or liberty (FP minimization)?

**Deontology/Rights-Based:**
- Respect individual rights (e.g., liberty, due process)
- May prioritize FP minimization (wrongful detention violates rights)
- Categorical imperative: Don't use race if you wouldn't want race used against you

**Rawlsian Justice:**
- Maximize outcomes for worst-off group (maximin principle)
- Prioritize reducing disparities
- May accept lower overall accuracy for improved fairness

**Virtue Ethics:**
- Emphasize character and deliberation
- Fairness as contextual, requiring practical wisdom
- Procedural justice: Are processes fair, even if outcomes differ?

**Critical Race Theory:**
- Examine structural racism embedded in institutions
- Question whether "fairness" is achievable in unjust system
- May advocate for abolition rather than algorithmic reform

**Our Stance:**
- We do not privilege one philosophical framework
- We present findings relevant to multiple frameworks
- We encourage readers to engage with normative questions

---

## 7. Potential for Harm

### 7.1 Direct Harms

**Harms to Individuals:**
1. **Liberty deprivation:** Wrongful detention from false positives
2. **Psychological harm:** Stigma of "high risk" label
3. **Privacy violations:** Data collection and inference
4. **Reduced autonomy:** Algorithmic predictions override individual narrative
5. **Procedural injustice:** Opaque predictions violate due process norms

**Harms to Groups:**
6. **Disparate impact:** Higher FP rates for marginalized groups
7. **Reinforcement of stereotypes:** "Black defendants are high risk"
8. **Community surveillance:** Concentrated prediction in over-policed areas
9. **Erosion of trust:** Algorithmic tools seen as illegitimate

### 7.2 Indirect and Systemic Harms

**Feedback Loops:**
1. **Prediction → Policing → Data:** High-risk labels lead to more surveillance → More arrests → More "recidivism" → Confirms predictions
2. **Self-fulfilling prophecies:** Denied opportunities → Increased strain → Higher actual recidivism
3. **Cumulative disadvantage:** Initial FP → Detention → Job loss → Housing loss → Desperation → Crime

**Institutional Harms:**
4. **Automation bias:** Over-reliance on algorithmic predictions, reduced human judgment
5. **Accountability diffusion:** "The algorithm made me do it"
6. **Resistance to reform:** Tools entrench status quo, reduce political will for change

**Societal Harms:**
7. **Normalization of surveillance:** Algorithmic prediction becomes expected
8. **Techno-solutionism:** Belief that algorithms can "solve" crime ignores root causes (poverty, inequality, lack of opportunity)
9. **Distraction from alternatives:** Energy spent on algorithmic fairness, not on reducing incarceration

### 7.3 Unintended Consequences

**Possible Negative Outcomes of Our Research:**

1. **Legitimation:** Publishing in top venues may legitimize predictive tools we critique
2. **Misuse:** Results cherry-picked to support deployment we oppose
3. **Commercial exploitation:** Vendors cite our research to sell products
4. **Scope creep:** Tools designed for pre-trial expand to sentencing, parole, policing
5. **International harms:** Tools exported to countries with weaker civil liberties protections
6. **Chilling effects:** Marginalized communities further disengaged from criminal justice system

**Mitigation:**
- Explicit "NOT recommended for deployment" statements
- Limitations prominently displayed
- Engagement with abolitionist perspectives
- Openness to criticism that research itself is harmful

---

## 8. Mitigation Strategies

### 8.1 Research Design Mitigations

**Transparency:**
1. **Open Code:** All code on GitHub, fully documented
2. **Open Data:** Use publicly available COMPAS data
3. **Pre-registration:** Analysis plan committed before results
4. **Research Log:** Document all analyses, including failures

**Fairness:**
5. **Comprehensive Auditing:** Fairlearn + Aequitas + custom metrics
6. **Intersectional Analysis:** Race × sex × age combinations
7. **Group-Specific Reporting:** Metrics for each demographic group
8. **Threshold Analysis:** Show impacts of different decision thresholds

**Humility:**
9. **Explicit Limitations:** Prominently displayed in abstract, intro, discussion
10. **No Deployment Claims:** Repeatedly state "benchmark only"
11. **Acknowledge Complicity:** We are part of the problem
12. **Engage Critics:** Cite abolitionist and critical perspectives

### 8.2 Communication Mitigations

**Academic Audiences:**
- Present at venues receptive to critical perspectives (FAccT, EAAMO)
- Seek out critical feedback
- Co-author with domain experts (criminologists, legal scholars)

**Policy Audiences:**
- Emphasize limitations, not performance gains
- Discuss structural alternatives (e.g., reducing incarceration, addressing root causes)
- Provide plain-language summaries

**Public Audiences:**
- Media training on responsible framing
- Decline interviews that sensationalize findings
- Correct misrepresentations of research

**Commercial Entities:**
- Explicit license prohibiting commercial use (consider CC BY-NC-SA)
- Do not consult for predictive policing vendors
- Publicly oppose misuse of research

### 8.3 Ongoing Ethical Review

**Checkpoints:**
1. **Before first analysis:** Ethics board review (if available)
2. **After preliminary results:** Consult with community organizations
3. **Before manuscript submission:** Fairness and ethics co-author review
4. **After acceptance:** Public comment period
5. **Post-publication:** Monitor citations and uses, issue corrections if misused

**Red Lines (will halt research):**
- Evidence that research is being used to increase incarceration
- Stakeholder outcry from affected communities
- Realization that harms outweigh benefits

---

## 9. Limitations and Transparency

### 9.1 Methodological Limitations

**Data Limitations:**
1. **Historical bias:** Data reflects discriminatory past
2. **Construct validity:** Recidivism is a noisy proxy
3. **Generalizability:** COMPAS is one county, one time period
4. **Missing variables:** Socioeconomic context, neighborhood, support systems
5. **Measurement error:** Recidivism depends on detection, not just behavior

**Model Limitations:**
6. **Correlation, not causation:** Cannot infer causal effects
7. **Fairness-accuracy tradeoffs:** No Pareto optimal solution
8. **Interpretability:** TabPFN less interpretable than logistic regression
9. **Overfitting:** Risk of capitalizing on noise in small datasets
10. **Distributional shift:** Models may not generalize to new contexts

**Evaluation Limitations:**
11. **Metrics are proxies:** AUROC doesn't capture real-world impact
12. **Threshold dependence:** Performance varies by decision threshold
13. **Short-term outcomes:** Two-year recidivism may not reflect long-term trajectories
14. **No counterfactuals:** Can't observe what would happen without prediction

### 9.2 Ethical Limitations

**Scope Limitations:**
1. **No stakeholder engagement:** Research conducted without input from affected communities
2. **Researcher positionality:** We are academics, not practitioners or affected individuals
3. **Institutional context:** Research may be appropriated by criminal justice agencies
4. **Power dynamics:** Subjects of prediction have no voice in research design

**Normative Limitations:**
5. **Fairness metrics are contested:** No consensus on "fair"
6. **Values embedded in choices:** Every decision (metrics, thresholds, features) embeds values
7. **Cannot solve structural problems:** Algorithms can't fix systemic inequality
8. **Reform vs abolition:** Research assumes predictive tools are legitimate (debatable)

### 9.3 Disclosure Statement

**We explicitly state:**

"This research evaluates TabPFN on criminal justice prediction as a **benchmark comparison only**. We do NOT recommend deployment of these or any predictive models in criminal justice without:

1. Extensive stakeholder engagement
2. Rigorous fairness auditing
3. Contestability mechanisms
4. Ongoing monitoring and evaluation
5. Consideration of structural alternatives to prediction (e.g., reducing incarceration, addressing root causes of crime)

We acknowledge that even benchmark research may legitimize tools we critique. Our goal is to advance methodological rigor in evaluating these tools, not to advocate for their use."

---

## 10. Responsible Deployment (Aspirational)

**Note:** Our research does NOT involve deployment. This section outlines what WOULD be needed if our findings were ever to inform practice.

### 10.1 Pre-Deployment Requirements

**Before ANY deployment:**

1. **Community Consent:** Affected communities must be informed and consent
2. **Impact Assessment:** Full algorithmic impact assessment (bias, privacy, fairness)
3. **Pilot Study:** Small-scale, monitored pilot with independent evaluation
4. **Legal Review:** Ensure compliance with anti-discrimination law
5. **Governance Structure:** Clear oversight, accountability, and appeal processes

### 10.2 Deployment Safeguards

**If deployed (hypothetically):**

1. **Human Override:** Humans must be able to override predictions with justification
2. **Transparency:** Individuals must know a prediction was made and how it was used
3. **Contestability:** Mechanisms for challenging predictions
4. **Monitoring:** Ongoing auditing of fairness, accuracy, and disparate impact
5. **Sunset Clause:** Automatic expiration unless renewed with evidence of benefit

### 10.3 Alternatives to Prediction

**We advocate for considering alternatives:**

1. **Structural reforms:**
   - Reduce reliance on cash bail (eliminates need for pre-trial risk assessment)
   - Decriminalize low-level offenses
   - Invest in community-based interventions

2. **Actuarial alternatives:**
   - Simple, transparent checklists (vs complex models)
   - Structured professional judgment
   - Evidence-based risk-needs assessment for rehabilitation (not punishment)

3. **Procedural justice:**
   - Improve fairness of legal processes
   - Reduce prosecutorial discretion
   - Eliminate mandatory minimums

---

## 11. Community Engagement

### 11.1 Engagement Principles

**We commit to (future work):**

1. **Nothing About Us Without Us:** Affected communities must have voice in research
2. **Power Sharing:** Co-design research questions, methods, interpretations
3. **Capacity Building:** Transfer knowledge and skills to communities
4. **Action Orientation:** Research should support community-defined goals
5. **Long-Term Relationships:** Not extractive, one-off studies

### 11.2 Recommended Engagement Strategies

**For future research or deployment:**

1. **Community Advisory Board:** Representatives from affected communities
2. **Focus Groups:** Formerly incarcerated individuals, families, community members
3. **Participatory Design:** Co-create interventions, not just evaluate existing tools
4. **Public Forums:** Present findings, receive feedback
5. **Co-Authorship:** Include community members as co-authors

### 11.3 Engagement Limitations in Current Work

**We acknowledge:**

This research was conducted without extensive community engagement due to time and resource constraints. This is a significant limitation.

**Future work should:**
- Partner with community organizations from inception
- Compensate community members for their expertise
- Be accountable to affected communities, not just academic gatekeepers

---

## 12. Ongoing Ethical Review

### 12.1 Commitment to Reflection

**Ethical review is not one-time:**

We commit to:
1. **Regular review:** Revisit ethical considerations at each project phase
2. **Responsiveness:** Adapt to new information and community feedback
3. **Accountability:** Take responsibility for harms, intended or not
4. **Learning:** Engage with ethical critiques, even if uncomfortable

### 12.2 Ethical Red Flags

**We will pause or halt research if:**

1. Evidence emerges that research is being misused to increase incarceration
2. Affected communities express strong opposition
3. Harms exceed benefits
4. Collaborators engage in unethical practices
5. Legal or regulatory landscape changes (e.g., ban on algorithmic risk assessment)

### 12.3 Continuous Improvement

**Living Document:**

This ethical framework will be updated as:
- New ethical considerations emerge
- We receive feedback from communities and colleagues
- Legal and policy context evolves
- Research findings raise new ethical questions

**Version Control:**
All updates documented in git history with justification.

---

## 13. Conclusion

**Research in criminal justice prediction is ethically fraught.**

Every choice—from data selection to metric definition to interpretation—embeds values and has potential for harm. We cannot eliminate these ethical tensions, but we can:

1. **Acknowledge them:** Transparent about limitations and potential harms
2. **Interrogate them:** Critically examine our assumptions and choices
3. **Engage them:** Invite diverse perspectives, especially from affected communities
4. **Mitigate them:** Take concrete steps to reduce harm

**Our commitment:**

We strive to conduct this research with **humility, transparency, and accountability**. We recognize that our work may be complicit in systems of oppression, even as we seek to critique them. We welcome critical feedback and commit to ongoing ethical reflection.

**Ultimately:**

We believe this research can contribute to methodological rigor in evaluating criminal justice predictions, but it is **not a solution** to the profound structural inequities in the criminal justice system. Those require political, economic, and social transformation—not just better algorithms.

---

## References

Angwin, J., Larson, J., Mattu, S., & Kirchner, L. (2016). Machine Bias. ProPublica.

Barocas, S., Hardt, M., & Narayanan, A. (2019). Fairness and Machine Learning. fairmlbook.org.

Chouldechova, A. (2017). Fair prediction with disparate impact: A study of bias in recidivism prediction instruments. Big Data, 5(2), 153-163.

Corbett-Davies, S., & Goel, S. (2018). The measure and mismeasure of fairness: A critical review of fair machine learning. arXiv preprint arXiv:1808.00023.

Kleinberg, J., Mullainathan, S., & Raghavan, M. (2017). Inherent trade-offs in the fair determination of risk scores. ITCS.

Rudin, C., Wang, C., & Coker, B. (2020). The age of secrecy and unfairness in recidivism prediction. Harvard Data Science Review, 2(1).

Selbst, A. D., Boyd, D., Friedler, S. A., Venkatasubramanian, S., & Vertesi, J. (2019). Fairness and abstraction in sociotechnical systems. In FAT* (pp. 59-68).

Starr, S. B. (2014). Evidence-based sentencing and the scientific rationalization of discrimination. Stanford Law Review, 66, 803.

---

**Document Version History:**
- v1.0 (2025-11-08): Initial ethical framework

**Authors:** [Research Team]

**Contact for Ethical Concerns:** [Email]

**Last Updated:** 2025-11-08
