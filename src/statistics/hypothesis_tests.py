"""Hypothesis testing utilities for model comparison.

This module provides statistical tests for comparing predictive models,
specifically tailored for criminal justice applications where careful
statistical inference is critical.

Functions:
    mcnemar_test: Test for paired model predictions (classification)
    delong_test: Test for comparing AUROCs
    permutation_test: Non-parametric test for arbitrary metrics
    bootstrap_test: Bootstrap-based hypothesis test
"""

from typing import Tuple, Optional, Dict, Any
import numpy as np
from scipy import stats
from sklearn.metrics import roc_auc_score, roc_curve


def mcnemar_test(
    y_true: np.ndarray,
    y_pred1: np.ndarray,
    y_pred2: np.ndarray,
    continuity_correction: bool = True,
) -> Dict[str, Any]:
    """McNemar's test for comparing two paired classifiers.

    Tests the null hypothesis that two classifiers have the same error rate
    on paired observations. Appropriate for comparing models trained on the
    same data and evaluated on the same test set.

    Parameters
    ----------
    y_true : np.ndarray, shape (n_samples,)
        True binary labels
    y_pred1 : np.ndarray, shape (n_samples,)
        Predictions from model 1 (binary)
    y_pred2 : np.ndarray, shape (n_samples,)
        Predictions from model 2 (binary)
    continuity_correction : bool, default=True
        Whether to apply continuity correction (recommended for small samples)

    Returns
    -------
    dict
        Dictionary containing:
        - statistic: Test statistic value
        - p_value: Two-tailed p-value
        - n_01: Number of cases where model 1 wrong, model 2 correct
        - n_10: Number of cases where model 1 correct, model 2 wrong
        - interpretation: String interpretation of result

    Notes
    -----
    The test statistic follows a chi-squared distribution with 1 degree of
    freedom under the null hypothesis.

    McNemar's test is preferred over simple accuracy comparison because it
    accounts for the paired nature of the predictions.

    References
    ----------
    McNemar, Q. (1947). Note on the sampling error of the difference between
    correlated proportions or percentages. Psychometrika, 12(2), 153-157.

    Examples
    --------
    >>> y_true = np.array([0, 1, 1, 0, 1])
    >>> y_pred1 = np.array([0, 1, 0, 0, 1])  # 80% accuracy
    >>> y_pred2 = np.array([0, 0, 1, 0, 1])  # 80% accuracy
    >>> result = mcnemar_test(y_true, y_pred1, y_pred2)
    >>> print(f"p-value: {result['p_value']:.4f}")
    """
    y_true = np.asarray(y_true)
    y_pred1 = np.asarray(y_pred1)
    y_pred2 = np.asarray(y_pred2)

    # Build contingency table
    correct1 = (y_pred1 == y_true).astype(int)
    correct2 = (y_pred2 == y_true).astype(int)

    # n_ij where i is model1 correctness, j is model2 correctness
    n_00 = np.sum((correct1 == 0) & (correct2 == 0))  # Both wrong
    n_01 = np.sum((correct1 == 0) & (correct2 == 1))  # Model1 wrong, Model2 correct
    n_10 = np.sum((correct1 == 1) & (correct2 == 0))  # Model1 correct, Model2 wrong
    n_11 = np.sum((correct1 == 1) & (correct2 == 1))  # Both correct

    # McNemar's test statistic
    if continuity_correction:
        statistic = (abs(n_01 - n_10) - 1) ** 2 / (n_01 + n_10) if (n_01 + n_10) > 0 else 0
    else:
        statistic = (n_01 - n_10) ** 2 / (n_01 + n_10) if (n_01 + n_10) > 0 else 0

    # P-value from chi-squared distribution
    p_value = 1 - stats.chi2.cdf(statistic, df=1)

    # Interpretation
    if p_value < 0.001:
        interpretation = "Very strong evidence of difference between models (p < 0.001)"
    elif p_value < 0.01:
        interpretation = "Strong evidence of difference between models (p < 0.01)"
    elif p_value < 0.05:
        interpretation = "Moderate evidence of difference between models (p < 0.05)"
    else:
        interpretation = "No significant difference between models (p >= 0.05)"

    return {
        "statistic": statistic,
        "p_value": p_value,
        "n_00": n_00,
        "n_01": n_01,
        "n_10": n_10,
        "n_11": n_11,
        "interpretation": interpretation,
        "test_name": "McNemar's Test",
        "correction": "continuity" if continuity_correction else "none",
    }


def delong_test(
    y_true: np.ndarray,
    y_score1: np.ndarray,
    y_score2: np.ndarray,
) -> Dict[str, Any]:
    """DeLong's test for comparing two ROC AUCs.

    Non-parametric test for the null hypothesis that two correlated AUROCs
    are equal. Accounts for correlation between models trained/evaluated on
    the same data.

    Parameters
    ----------
    y_true : np.ndarray, shape (n_samples,)
        True binary labels
    y_score1 : np.ndarray, shape (n_samples,)
        Predicted scores/probabilities from model 1
    y_score2 : np.ndarray, shape (n_samples,)
        Predicted scores/probabilities from model 2

    Returns
    -------
    dict
        Dictionary containing:
        - auc1: AUROC for model 1
        - auc2: AUROC for model 2
        - auc_diff: Difference in AUROCs
        - statistic: Z-statistic
        - p_value: Two-tailed p-value
        - interpretation: String interpretation

    Notes
    -----
    DeLong's test is the appropriate test for comparing AUROCs from paired
    predictions, as it accounts for the correlation structure.

    References
    ----------
    DeLong, E. R., DeLong, D. M., & Clarke-Pearson, D. L. (1988).
    Comparing the areas under two or more correlated receiver operating
    characteristic curves: a nonparametric approach. Biometrics, 837-845.

    Examples
    --------
    >>> y_true = np.array([0, 1, 1, 0, 1])
    >>> y_score1 = np.array([0.2, 0.8, 0.7, 0.3, 0.9])
    >>> y_score2 = np.array([0.3, 0.6, 0.8, 0.2, 0.85])
    >>> result = delong_test(y_true, y_score1, y_score2)
    >>> print(f"AUROC difference: {result['auc_diff']:.4f}, p={result['p_value']:.4f}")
    """
    y_true = np.asarray(y_true)
    y_score1 = np.asarray(y_score1)
    y_score2 = np.asarray(y_score2)

    # Calculate AUROCs
    auc1 = roc_auc_score(y_true, y_score1)
    auc2 = roc_auc_score(y_true, y_score2)
    auc_diff = auc1 - auc2

    # Simplified DeLong implementation
    # For full implementation, use scipy or dedicated library
    # This is a placeholder that uses normal approximation

    n_pos = np.sum(y_true == 1)
    n_neg = np.sum(y_true == 0)

    # Compute variance using structural components
    # (simplified version - full DeLong requires structural components)
    var_auc1 = _auc_variance(y_true, y_score1, auc1)
    var_auc2 = _auc_variance(y_true, y_score2, auc2)
    cov_auc = _auc_covariance(y_true, y_score1, y_score2)

    # Variance of difference
    var_diff = var_auc1 + var_auc2 - 2 * cov_auc

    # Z-statistic
    if var_diff > 0:
        z_stat = auc_diff / np.sqrt(var_diff)
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    else:
        z_stat = 0
        p_value = 1.0

    # Interpretation
    if p_value < 0.001:
        interpretation = f"Very strong evidence that AUROCs differ (p < 0.001)"
    elif p_value < 0.01:
        interpretation = f"Strong evidence that AUROCs differ (p < 0.01)"
    elif p_value < 0.05:
        interpretation = f"Moderate evidence that AUROCs differ (p < 0.05)"
    else:
        interpretation = f"No significant difference in AUROCs (p >= 0.05)"

    return {
        "auc1": auc1,
        "auc2": auc2,
        "auc_diff": auc_diff,
        "statistic": z_stat,
        "p_value": p_value,
        "interpretation": interpretation,
        "test_name": "DeLong's Test",
        "note": "Simplified implementation - for production use scipy or pROC",
    }


def _auc_variance(y_true: np.ndarray, y_score: np.ndarray, auc: float) -> float:
    """Estimate variance of AUC using Hanley-McNeil formula."""
    n_pos = np.sum(y_true == 1)
    n_neg = np.sum(y_true == 0)

    q1 = auc / (2 - auc)
    q2 = 2 * auc**2 / (1 + auc)

    var_auc = (auc * (1 - auc) + (n_pos - 1) * (q1 - auc**2) +
               (n_neg - 1) * (q2 - auc**2)) / (n_pos * n_neg)

    return var_auc


def _auc_covariance(y_true: np.ndarray, y_score1: np.ndarray, y_score2: np.ndarray) -> float:
    """Estimate covariance between two AUCs (simplified)."""
    # Simplified covariance estimation
    # Full DeLong requires structural components
    auc1 = roc_auc_score(y_true, y_score1)
    auc2 = roc_auc_score(y_true, y_score2)

    # Approximate using correlation between scores
    # This is a simplification - full implementation is more complex
    corr = np.corrcoef(y_score1, y_score2)[0, 1]
    var_auc1 = _auc_variance(y_true, y_score1, auc1)
    var_auc2 = _auc_variance(y_true, y_score2, auc2)

    cov = corr * np.sqrt(var_auc1 * var_auc2)
    return cov


def permutation_test(
    y_true: np.ndarray,
    y_pred1: np.ndarray,
    y_pred2: np.ndarray,
    metric_func: callable,
    n_permutations: int = 10000,
    random_state: Optional[int] = None,
) -> Dict[str, Any]:
    """Permutation test for comparing two models on arbitrary metric.

    Non-parametric test that doesn't make distributional assumptions.
    Tests whether the difference in performance between two models is
    significant by randomly permuting the model labels.

    Parameters
    ----------
    y_true : np.ndarray
        True labels
    y_pred1 : np.ndarray
        Predictions from model 1
    y_pred2 : np.ndarray
        Predictions from model 2
    metric_func : callable
        Function that takes (y_true, y_pred) and returns a scalar metric
    n_permutations : int, default=10000
        Number of permutations for null distribution
    random_state : int, optional
        Random seed for reproducibility

    Returns
    -------
    dict
        Dictionary containing test results

    Examples
    --------
    >>> from sklearn.metrics import accuracy_score
    >>> result = permutation_test(y_true, y_pred1, y_pred2, accuracy_score)
    """
    rng = np.random.RandomState(random_state)

    # Observed difference
    metric1 = metric_func(y_true, y_pred1)
    metric2 = metric_func(y_true, y_pred2)
    observed_diff = metric1 - metric2

    # Generate null distribution by permuting labels
    null_diffs = []
    for _ in range(n_permutations):
        # Randomly swap predictions between models
        swap_mask = rng.rand(len(y_pred1)) < 0.5
        perm_pred1 = np.where(swap_mask, y_pred2, y_pred1)
        perm_pred2 = np.where(swap_mask, y_pred1, y_pred2)

        perm_metric1 = metric_func(y_true, perm_pred1)
        perm_metric2 = metric_func(y_true, perm_pred2)
        null_diffs.append(perm_metric1 - perm_metric2)

    null_diffs = np.array(null_diffs)

    # Two-tailed p-value
    p_value = np.mean(np.abs(null_diffs) >= np.abs(observed_diff))

    # Interpretation
    if p_value < 0.001:
        interpretation = "Very strong evidence of difference (p < 0.001)"
    elif p_value < 0.01:
        interpretation = "Strong evidence of difference (p < 0.01)"
    elif p_value < 0.05:
        interpretation = "Moderate evidence of difference (p < 0.05)"
    else:
        interpretation = "No significant difference (p >= 0.05)"

    return {
        "metric1": metric1,
        "metric2": metric2,
        "observed_diff": observed_diff,
        "p_value": p_value,
        "n_permutations": n_permutations,
        "null_distribution": null_diffs,
        "interpretation": interpretation,
        "test_name": "Permutation Test",
    }


def bootstrap_test(
    y_true: np.ndarray,
    y_pred1: np.ndarray,
    y_pred2: np.ndarray,
    metric_func: callable,
    n_bootstrap: int = 10000,
    confidence_level: float = 0.95,
    random_state: Optional[int] = None,
) -> Dict[str, Any]:
    """Bootstrap test for comparing two models.

    Constructs bootstrap confidence interval for the difference in metrics
    between two models. If the CI excludes zero, there is significant
    difference at the specified confidence level.

    Parameters
    ----------
    y_true : np.ndarray
        True labels
    y_pred1 : np.ndarray
        Predictions from model 1
    y_pred2 : np.ndarray
        Predictions from model 2
    metric_func : callable
        Function that takes (y_true, y_pred) and returns a scalar metric
    n_bootstrap : int, default=10000
        Number of bootstrap iterations
    confidence_level : float, default=0.95
        Confidence level for interval (0.95 = 95%)
    random_state : int, optional
        Random seed

    Returns
    -------
    dict
        Dictionary containing test results and confidence intervals

    Examples
    --------
    >>> from sklearn.metrics import f1_score
    >>> result = bootstrap_test(y_true, y_pred1, y_pred2, f1_score)
    >>> print(f"95% CI: [{result['ci_lower']:.3f}, {result['ci_upper']:.3f}]")
    """
    rng = np.random.RandomState(random_state)

    n = len(y_true)

    # Observed difference
    metric1 = metric_func(y_true, y_pred1)
    metric2 = metric_func(y_true, y_pred2)
    observed_diff = metric1 - metric2

    # Bootstrap distribution
    boot_diffs = []
    for _ in range(n_bootstrap):
        # Resample with replacement
        indices = rng.choice(n, size=n, replace=True)

        boot_metric1 = metric_func(y_true[indices], y_pred1[indices])
        boot_metric2 = metric_func(y_true[indices], y_pred2[indices])
        boot_diffs.append(boot_metric1 - boot_metric2)

    boot_diffs = np.array(boot_diffs)

    # Confidence interval
    alpha = 1 - confidence_level
    ci_lower = np.percentile(boot_diffs, 100 * alpha / 2)
    ci_upper = np.percentile(boot_diffs, 100 * (1 - alpha / 2))

    # Check if CI excludes zero
    significant = not (ci_lower <= 0 <= ci_upper)

    # Interpretation
    if significant:
        interpretation = f"Significant difference at {confidence_level*100}% level (CI excludes 0)"
    else:
        interpretation = f"No significant difference at {confidence_level*100}% level (CI includes 0)"

    return {
        "metric1": metric1,
        "metric2": metric2,
        "observed_diff": observed_diff,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "confidence_level": confidence_level,
        "significant": significant,
        "boot_distribution": boot_diffs,
        "n_bootstrap": n_bootstrap,
        "interpretation": interpretation,
        "test_name": "Bootstrap Test",
    }
