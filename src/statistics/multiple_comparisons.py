"""Multiple comparisons correction methods.

When conducting multiple statistical tests (e.g., comparing many models across
many fairness metrics), the probability of finding at least one false positive
increases. These corrections control error rates.

Functions:
    bonferroni_correction: Conservative family-wise error rate control
    holm_correction: Less conservative step-down method
    benjamini_hochberg: False discovery rate control
    false_discovery_rate: Estimate FDR from p-values
"""

from typing import List, Tuple, Dict, Optional
import numpy as np


def bonferroni_correction(
    p_values: np.ndarray,
    alpha: float = 0.05,
) -> Dict[str, np.ndarray]:
    """Apply Bonferroni correction for multiple comparisons.

    Most conservative method. Controls family-wise error rate (FWER):
    the probability of making ANY false rejections.

    Parameters
    ----------
    p_values : np.ndarray
        Array of p-values from multiple tests
    alpha : float, default=0.05
        Desired family-wise error rate

    Returns
    -------
    dict
        Dictionary containing:
        - corrected_alpha: Adjusted significance threshold
        - reject: Boolean array indicating which hypotheses to reject
        - adjusted_p_values: Bonferroni-adjusted p-values

    Notes
    -----
    Adjusted significance level: alpha / m, where m is number of tests.

    Very conservative - may miss true effects when many tests are performed.
    Best when false positives are very costly.

    References
    ----------
    Bonferroni, C. (1936). Teoria statistica delle classi e calcolo delle
    probabilità. Pubblicazioni del R Istituto Superiore di Scienze Economiche
    e Commericiali di Firenze, 8, 3-62.

    Examples
    --------
    >>> p_vals = np.array([0.01, 0.03, 0.07, 0.001, 0.15])
    >>> result = bonferroni_correction(p_vals, alpha=0.05)
    >>> print(f"Reject: {result['reject']}")
    >>> print(f"Adjusted threshold: {result['corrected_alpha']:.4f}")
    """
    p_values = np.asarray(p_values)
    m = len(p_values)

    # Corrected significance level
    corrected_alpha = alpha / m

    # Adjusted p-values (multiply by number of tests, cap at 1.0)
    adjusted_p_values = np.minimum(p_values * m, 1.0)

    # Rejection decisions
    reject = adjusted_p_values < alpha

    return {
        "corrected_alpha": corrected_alpha,
        "reject": reject,
        "adjusted_p_values": adjusted_p_values,
        "n_tests": m,
        "n_rejected": np.sum(reject),
        "method": "Bonferroni",
    }


def holm_correction(
    p_values: np.ndarray,
    alpha: float = 0.05,
) -> Dict[str, np.ndarray]:
    """Apply Holm-Bonferroni step-down correction.

    Less conservative than Bonferroni while still controlling FWER.
    Uses step-down procedure with increasing thresholds.

    Parameters
    ----------
    p_values : np.ndarray
        Array of p-values from multiple tests
    alpha : float, default=0.05
        Desired family-wise error rate

    Returns
    -------
    dict
        Dictionary containing rejection decisions and adjusted p-values

    Notes
    -----
    Step-down procedure:
    1. Sort p-values from smallest to largest
    2. Compare each to alpha/(m-i+1) where i is rank
    3. Stop at first non-rejection

    More powerful than Bonferroni but still controls FWER.

    References
    ----------
    Holm, S. (1979). A simple sequentially rejective multiple test procedure.
    Scandinavian Journal of Statistics, 6(2), 65-70.

    Examples
    --------
    >>> p_vals = np.array([0.01, 0.03, 0.07, 0.001, 0.15])
    >>> result = holm_correction(p_vals, alpha=0.05)
    >>> print(f"Reject: {result['reject']}")
    """
    p_values = np.asarray(p_values)
    m = len(p_values)

    # Sort p-values and track original indices
    sorted_indices = np.argsort(p_values)
    sorted_p_values = p_values[sorted_indices]

    # Adjusted p-values using step-down
    adjusted_p_values = np.zeros(m)
    cumulative_min = 0

    for i, p in enumerate(sorted_p_values):
        # Holm adjustment
        adjusted_p = p * (m - i)
        # Take cumulative maximum to ensure monotonicity
        adjusted_p = max(adjusted_p, cumulative_min)
        # Cap at 1.0
        adjusted_p = min(adjusted_p, 1.0)

        adjusted_p_values[sorted_indices[i]] = adjusted_p
        cumulative_min = adjusted_p

    # Rejection decisions
    reject = adjusted_p_values < alpha

    return {
        "reject": reject,
        "adjusted_p_values": adjusted_p_values,
        "n_tests": m,
        "n_rejected": np.sum(reject),
        "method": "Holm-Bonferroni",
    }


def benjamini_hochberg(
    p_values: np.ndarray,
    alpha: float = 0.05,
) -> Dict[str, np.ndarray]:
    """Apply Benjamini-Hochberg FDR correction.

    Controls False Discovery Rate (FDR): expected proportion of false
    positives among all rejections.

    Less conservative than FWER methods, appropriate when some false
    positives are acceptable in exchange for higher power.

    Parameters
    ----------
    p_values : np.ndarray
        Array of p-values from multiple tests
    alpha : float, default=0.05
        Desired false discovery rate

    Returns
    -------
    dict
        Dictionary containing rejection decisions and adjusted p-values

    Notes
    -----
    Step-up procedure:
    1. Sort p-values from smallest to largest
    2. Find largest i where p(i) <= (i/m) * alpha
    3. Reject all hypotheses up to i

    FDR control is less stringent than FWER, allowing more discoveries.
    Appropriate for exploratory research.

    References
    ----------
    Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery
    rate: a practical and powerful approach to multiple testing.
    Journal of the Royal Statistical Society, Series B, 57(1), 289-300.

    Examples
    --------
    >>> p_vals = np.array([0.01, 0.03, 0.07, 0.001, 0.15])
    >>> result = benjamini_hochberg(p_vals, alpha=0.05)
    >>> print(f"Reject: {result['reject']}")
    >>> print(f"Estimated FDR: {result['estimated_fdr']:.3f}")
    """
    p_values = np.asarray(p_values)
    m = len(p_values)

    # Sort p-values and track original indices
    sorted_indices = np.argsort(p_values)
    sorted_p_values = p_values[sorted_indices]

    # Calculate critical values: (i/m) * alpha
    ranks = np.arange(1, m + 1)
    critical_values = (ranks / m) * alpha

    # Find largest i where p(i) <= critical_value(i)
    significant = sorted_p_values <= critical_values
    if np.any(significant):
        max_index = np.where(significant)[0][-1]
        reject_sorted = np.zeros(m, dtype=bool)
        reject_sorted[:max_index + 1] = True
    else:
        reject_sorted = np.zeros(m, dtype=bool)

    # Map back to original order
    reject = np.zeros(m, dtype=bool)
    reject[sorted_indices] = reject_sorted

    # Adjusted p-values
    adjusted_p_values = np.zeros(m)
    cumulative_min = 1.0

    for i in range(m - 1, -1, -1):
        # BH adjustment
        adjusted_p = sorted_p_values[i] * m / (i + 1)
        # Take cumulative minimum (reverse direction)
        adjusted_p = min(adjusted_p, cumulative_min)
        # Cap at 1.0
        adjusted_p = min(adjusted_p, 1.0)

        adjusted_p_values[sorted_indices[i]] = adjusted_p
        cumulative_min = adjusted_p

    # Estimate FDR
    n_rejected = np.sum(reject)
    if n_rejected > 0:
        estimated_fdr = np.sum(adjusted_p_values[reject]) / n_rejected
    else:
        estimated_fdr = 0.0

    return {
        "reject": reject,
        "adjusted_p_values": adjusted_p_values,
        "n_tests": m,
        "n_rejected": n_rejected,
        "estimated_fdr": estimated_fdr,
        "method": "Benjamini-Hochberg",
    }


def false_discovery_rate(
    p_values: np.ndarray,
    rejected: Optional[np.ndarray] = None,
    alpha: float = 0.05,
) -> float:
    """Estimate false discovery rate from p-values.

    Estimates the proportion of false positives among rejected hypotheses.

    Parameters
    ----------
    p_values : np.ndarray
        Array of p-values from multiple tests
    rejected : np.ndarray, optional
        Boolean array indicating which hypotheses were rejected.
        If None, uses p_values < alpha.
    alpha : float, default=0.05
        Significance threshold (used if rejected is None)

    Returns
    -------
    float
        Estimated FDR (between 0 and 1)

    Notes
    -----
    Storey's q-value method for FDR estimation.

    FDR = 0 means no false positives expected.
    FDR = 0.05 means 5% of rejections expected to be false positives.

    Examples
    --------
    >>> p_vals = np.array([0.001, 0.01, 0.03, 0.08, 0.15])
    >>> rejected = p_vals < 0.05
    >>> fdr = false_discovery_rate(p_vals, rejected)
    >>> print(f"Estimated FDR: {fdr:.3f}")
    """
    p_values = np.asarray(p_values)
    m = len(p_values)

    if rejected is None:
        rejected = p_values < alpha

    n_rejected = np.sum(rejected)

    if n_rejected == 0:
        return 0.0

    # Storey's q-value estimation
    # Estimate proportion of true nulls (pi0)
    lambda_val = 0.5  # Conservative choice
    pi0 = np.sum(p_values > lambda_val) / ((1 - lambda_val) * m)
    pi0 = min(pi0, 1.0)  # Cap at 1

    # Estimate FDR
    fdr = (pi0 * m * alpha) / max(n_rejected, 1)
    fdr = min(fdr, 1.0)  # Cap at 1

    return fdr


def compare_correction_methods(
    p_values: np.ndarray,
    alpha: float = 0.05,
) -> Dict[str, Dict]:
    """Compare different multiple testing correction methods.

    Useful for understanding the tradeoffs between conservative (FWER)
    and liberal (FDR) approaches.

    Parameters
    ----------
    p_values : np.ndarray
        Array of p-values from multiple tests
    alpha : float, default=0.05
        Significance level

    Returns
    -------
    dict
        Dictionary with results from each method

    Examples
    --------
    >>> p_vals = np.array([0.001, 0.01, 0.03, 0.05, 0.08, 0.15])
    >>> comparison = compare_correction_methods(p_vals)
    >>> for method, results in comparison.items():
    ...     print(f"{method}: {results['n_rejected']} rejections")
    """
    results = {
        "uncorrected": {
            "reject": p_values < alpha,
            "n_rejected": np.sum(p_values < alpha),
            "method": "Uncorrected",
        },
        "bonferroni": bonferroni_correction(p_values, alpha),
        "holm": holm_correction(p_values, alpha),
        "benjamini_hochberg": benjamini_hochberg(p_values, alpha),
    }

    # Add FDR estimate for each method
    for method, res in results.items():
        if method != "uncorrected":
            res["estimated_fdr"] = false_discovery_rate(
                p_values, res["reject"], alpha
            )

    return results


def interpret_corrections(comparison_results: Dict[str, Dict]) -> str:
    """Generate interpretation of correction method comparison.

    Parameters
    ----------
    comparison_results : dict
        Output from compare_correction_methods()

    Returns
    -------
    str
        Human-readable interpretation

    Examples
    --------
    >>> p_vals = np.array([0.001, 0.01, 0.03, 0.05, 0.08])
    >>> results = compare_correction_methods(p_vals)
    >>> print(interpret_corrections(results))
    """
    uncorr = comparison_results["uncorrected"]["n_rejected"]
    bonf = comparison_results["bonferroni"]["n_rejected"]
    holm = comparison_results["holm"]["n_rejected"]
    bh = comparison_results["benjamini_hochberg"]["n_rejected"]

    interpretation = f"""
Multiple Testing Correction Summary:
------------------------------------
Uncorrected: {uncorr} rejections (no correction - inflated Type I error)
Bonferroni: {bonf} rejections (most conservative - controls FWER)
Holm: {holm} rejections (less conservative - controls FWER)
Benjamini-Hochberg: {bh} rejections (controls FDR, more powerful)

Recommendation:
- Use Bonferroni if false positives are very costly
- Use Holm for better power while controlling FWER
- Use Benjamini-Hochberg for exploratory research (some false positives acceptable)
    """

    return interpretation.strip()
