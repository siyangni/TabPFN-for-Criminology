"""Effect size calculations for criminal justice prediction models.

Effect sizes provide measures of practical significance beyond statistical
significance. These are critical for policy decisions where small p-values
may not indicate meaningful differences.

Functions:
    cohens_d: Standardized mean difference
    cohens_h: Difference between proportions
    cramers_v: Association strength for categorical variables
    risk_difference: Absolute risk difference
    risk_ratio: Relative risk ratio
    odds_ratio: Odds ratio with confidence intervals
    number_needed_to_evaluate: NNE for classification
"""

from typing import Tuple, Optional, Dict
import numpy as np
from scipy import stats


def cohens_d(
    group1: np.ndarray,
    group2: np.ndarray,
    pooled: bool = True,
) -> float:
    """Calculate Cohen's d effect size.

    Standardized mean difference between two groups. Commonly used to
    quantify the difference in model performance metrics between groups.

    Parameters
    ----------
    group1 : np.ndarray
        Values for group 1
    group2 : np.ndarray
        Values for group 2
    pooled : bool, default=True
        Whether to use pooled standard deviation

    Returns
    -------
    float
        Cohen's d effect size

    Notes
    -----
    Interpretation guidelines (Cohen, 1988):
    - Small effect: |d| = 0.2
    - Medium effect: |d| = 0.5
    - Large effect: |d| = 0.8

    References
    ----------
    Cohen, J. (1988). Statistical power analysis for the behavioral sciences
    (2nd ed.). Hillsdale, NJ: Lawrence Erlbaum Associates.

    Examples
    --------
    >>> accuracy_group1 = np.array([0.72, 0.75, 0.73, 0.74])
    >>> accuracy_group2 = np.array([0.68, 0.67, 0.69, 0.70])
    >>> d = cohens_d(accuracy_group1, accuracy_group2)
    >>> print(f"Cohen's d: {d:.3f}")
    """
    n1, n2 = len(group1), len(group2)
    mean1, mean2 = np.mean(group1), np.mean(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)

    if pooled:
        # Pooled standard deviation
        pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
        d = (mean1 - mean2) / pooled_std
    else:
        # Use std of group2 (control group)
        d = (mean1 - mean2) / np.sqrt(var2)

    return d


def cohens_h(p1: float, p2: float) -> float:
    """Calculate Cohen's h for difference in proportions.

    Measures effect size for the difference between two proportions,
    commonly used for comparing classification rates across groups.

    Parameters
    ----------
    p1 : float
        Proportion for group 1 (between 0 and 1)
    p2 : float
        Proportion for group 2 (between 0 and 1)

    Returns
    -------
    float
        Cohen's h effect size

    Notes
    -----
    Interpretation guidelines (Cohen, 1988):
    - Small effect: |h| = 0.2
    - Medium effect: |h| = 0.5
    - Large effect: |h| = 0.8

    Examples
    --------
    >>> # Compare positive prediction rates
    >>> h = cohens_h(0.65, 0.55)  # 65% vs 55%
    >>> print(f"Cohen's h: {h:.3f}")
    """
    # Arcsine transformation
    phi1 = 2 * np.arcsin(np.sqrt(p1))
    phi2 = 2 * np.arcsin(np.sqrt(p2))
    h = phi1 - phi2
    return h


def cramers_v(contingency_table: np.ndarray) -> float:
    """Calculate Cramér's V for association strength.

    Measures association between two categorical variables,
    commonly used for assessing fairness across multiple groups.

    Parameters
    ----------
    contingency_table : np.ndarray, shape (r, c)
        Contingency table with r rows and c columns

    Returns
    -------
    float
        Cramér's V (between 0 and 1)

    Notes
    -----
    Interpretation (general guidelines):
    - Small effect: V = 0.1
    - Medium effect: V = 0.3
    - Large effect: V = 0.5

    Examples
    --------
    >>> # Predicted vs True for two groups
    >>> table = np.array([[40, 10], [30, 20]])
    >>> v = cramers_v(table)
    >>> print(f"Cramér's V: {v:.3f}")
    """
    chi2 = stats.chi2_contingency(contingency_table)[0]
    n = contingency_table.sum()
    min_dim = min(contingency_table.shape) - 1

    v = np.sqrt(chi2 / (n * min_dim))
    return v


def risk_difference(
    n_events_treatment: int,
    n_total_treatment: int,
    n_events_control: int,
    n_total_control: int,
    confidence_level: float = 0.95,
) -> Dict[str, float]:
    """Calculate risk difference (RD) with confidence interval.

    Absolute difference in event rates between two groups.
    Critical for policy evaluation where absolute impacts matter.

    Parameters
    ----------
    n_events_treatment : int
        Number of events in treatment group
    n_total_treatment : int
        Total subjects in treatment group
    n_events_control : int
        Number of events in control group
    n_total_control : int
        Total subjects in control group
    confidence_level : float, default=0.95
        Confidence level for interval

    Returns
    -------
    dict
        Dictionary with RD and confidence interval

    Notes
    -----
    RD = P(event|treatment) - P(event|control)

    Positive RD indicates higher risk in treatment group.
    RD is preferred when absolute differences matter for policy.

    Examples
    --------
    >>> # False positive rates: 20/100 vs 10/100
    >>> result = risk_difference(20, 100, 10, 100)
    >>> print(f"RD: {result['rd']:.3f} [{result['ci_lower']:.3f}, {result['ci_upper']:.3f}]")
    """
    # Calculate proportions
    p1 = n_events_treatment / n_total_treatment
    p2 = n_events_control / n_total_control

    # Risk difference
    rd = p1 - p2

    # Standard error
    se = np.sqrt(
        (p1 * (1 - p1) / n_total_treatment) +
        (p2 * (1 - p2) / n_total_control)
    )

    # Confidence interval
    alpha = 1 - confidence_level
    z_crit = stats.norm.ppf(1 - alpha / 2)
    ci_lower = rd - z_crit * se
    ci_upper = rd + z_crit * se

    return {
        "rd": rd,
        "se": se,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "p1": p1,
        "p2": p2,
        "confidence_level": confidence_level,
    }


def risk_ratio(
    n_events_treatment: int,
    n_total_treatment: int,
    n_events_control: int,
    n_total_control: int,
    confidence_level: float = 0.95,
) -> Dict[str, float]:
    """Calculate risk ratio (RR) with confidence interval.

    Relative risk of event in treatment vs control group.
    Useful when comparing proportional increases in risk.

    Parameters
    ----------
    n_events_treatment : int
        Number of events in treatment group
    n_total_treatment : int
        Total subjects in treatment group
    n_events_control : int
        Number of events in control group
    n_total_control : int
        Total subjects in control group
    confidence_level : float, default=0.95
        Confidence level for interval

    Returns
    -------
    dict
        Dictionary with RR and confidence interval

    Notes
    -----
    RR = P(event|treatment) / P(event|control)

    RR = 1: Equal risk
    RR > 1: Increased risk in treatment
    RR < 1: Decreased risk in treatment

    Examples
    --------
    >>> result = risk_ratio(20, 100, 10, 100)
    >>> print(f"RR: {result['rr']:.3f} [{result['ci_lower']:.3f}, {result['ci_upper']:.3f}]")
    """
    # Calculate proportions
    p1 = n_events_treatment / n_total_treatment
    p2 = n_events_control / n_total_control

    # Risk ratio (avoid division by zero)
    if p2 == 0:
        rr = np.inf if p1 > 0 else 1.0
        log_rr = np.inf if p1 > 0 else 0.0
        se_log_rr = np.inf
    else:
        rr = p1 / p2
        log_rr = np.log(rr)

        # Standard error of log(RR)
        se_log_rr = np.sqrt(
            (1 - p1) / (n_events_treatment + 1e-10) +
            (1 - p2) / (n_events_control + 1e-10)
        )

    # Confidence interval on log scale
    alpha = 1 - confidence_level
    z_crit = stats.norm.ppf(1 - alpha / 2)

    if not np.isinf(se_log_rr):
        ci_lower = np.exp(log_rr - z_crit * se_log_rr)
        ci_upper = np.exp(log_rr + z_crit * se_log_rr)
    else:
        ci_lower = np.inf
        ci_upper = np.inf

    return {
        "rr": rr,
        "log_rr": log_rr,
        "se_log_rr": se_log_rr,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "p1": p1,
        "p2": p2,
        "confidence_level": confidence_level,
    }


def odds_ratio(
    n_events_treatment: int,
    n_total_treatment: int,
    n_events_control: int,
    n_total_control: int,
    confidence_level: float = 0.95,
) -> Dict[str, float]:
    """Calculate odds ratio (OR) with confidence interval.

    Ratio of odds of event in treatment vs control.
    Common in logistic regression and case-control studies.

    Parameters
    ----------
    n_events_treatment : int
        Number of events in treatment group
    n_total_treatment : int
        Total subjects in treatment group
    n_events_control : int
        Number of events in control group
    n_total_control : int
        Total subjects in control group
    confidence_level : float, default=0.95
        Confidence level for interval

    Returns
    -------
    dict
        Dictionary with OR and confidence interval

    Notes
    -----
    OR = [p1/(1-p1)] / [p2/(1-p2)]

    OR = 1: Equal odds
    OR > 1: Increased odds in treatment
    OR < 1: Decreased odds in treatment

    Examples
    --------
    >>> result = odds_ratio(20, 100, 10, 100)
    >>> print(f"OR: {result['or']:.3f} [{result['ci_lower']:.3f}, {result['ci_upper']:.3f}]")
    """
    # Calculate proportions
    p1 = n_events_treatment / n_total_treatment
    p2 = n_events_control / n_total_control

    # Odds
    odds1 = p1 / (1 - p1 + 1e-10)
    odds2 = p2 / (1 - p2 + 1e-10)

    # Odds ratio
    or_value = odds1 / (odds2 + 1e-10)
    log_or = np.log(or_value + 1e-10)

    # Standard error of log(OR)
    n_nonevents_treatment = n_total_treatment - n_events_treatment
    n_nonevents_control = n_total_control - n_events_control

    se_log_or = np.sqrt(
        1 / (n_events_treatment + 0.5) +
        1 / (n_nonevents_treatment + 0.5) +
        1 / (n_events_control + 0.5) +
        1 / (n_nonevents_control + 0.5)
    )

    # Confidence interval on log scale
    alpha = 1 - confidence_level
    z_crit = stats.norm.ppf(1 - alpha / 2)

    ci_lower = np.exp(log_or - z_crit * se_log_or)
    ci_upper = np.exp(log_or + z_crit * se_log_or)

    return {
        "or": or_value,
        "log_or": log_or,
        "se_log_or": se_log_or,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "odds1": odds1,
        "odds2": odds2,
        "confidence_level": confidence_level,
    }


def number_needed_to_evaluate(
    y_true: np.ndarray,
    y_pred_baseline: np.ndarray,
    y_pred_new: np.ndarray,
) -> Dict[str, float]:
    """Calculate Number Needed to Evaluate (NNE).

    Number of cases that need to be evaluated with the new model
    (instead of baseline) to observe one additional correct prediction.

    Parameters
    ----------
    y_true : np.ndarray
        True labels
    y_pred_baseline : np.ndarray
        Predictions from baseline model
    y_pred_new : np.ndarray
        Predictions from new model

    Returns
    -------
    dict
        Dictionary with NNE and related metrics

    Notes
    -----
    NNE = 1 / (accuracy_new - accuracy_baseline)

    Lower NNE indicates more practical benefit per case evaluated.

    Analogy to Number Needed to Treat (NNT) in medical research.

    Examples
    --------
    >>> y_true = np.array([0, 1, 1, 0, 1] * 100)
    >>> y_baseline = np.array([0, 1, 0, 0, 1] * 100)  # 60% accuracy
    >>> y_new = np.array([0, 1, 1, 0, 1] * 100)       # 80% accuracy
    >>> result = number_needed_to_evaluate(y_true, y_baseline, y_new)
    >>> print(f"NNE: {result['nne']:.1f}")
    """
    # Calculate accuracies
    acc_baseline = np.mean(y_pred_baseline == y_true)
    acc_new = np.mean(y_pred_new == y_true)

    # Absolute risk reduction (ARR)
    arr = acc_new - acc_baseline

    # Number needed to evaluate
    if arr > 0:
        nne = 1 / arr
    elif arr < 0:
        nne = 1 / arr  # Negative NNE indicates harm
    else:
        nne = np.inf  # No difference

    return {
        "nne": nne,
        "arr": arr,
        "accuracy_baseline": acc_baseline,
        "accuracy_new": acc_new,
        "interpretation": _interpret_nne(nne, arr),
    }


def _interpret_nne(nne: float, arr: float) -> str:
    """Interpret NNE value."""
    if np.isinf(nne):
        return "No difference between models"
    elif arr > 0:
        if nne < 10:
            return f"Large practical benefit: Only {nne:.1f} cases needed for 1 additional correct prediction"
        elif nne < 50:
            return f"Moderate practical benefit: {nne:.1f} cases needed for 1 additional correct prediction"
        else:
            return f"Small practical benefit: {nne:.1f} cases needed for 1 additional correct prediction"
    else:
        return f"New model performs worse: {abs(nne):.1f} cases for 1 additional error"
