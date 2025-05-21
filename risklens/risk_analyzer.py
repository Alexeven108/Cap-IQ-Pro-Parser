from scipy.stats import chi2
import numpy as np

# Function to calculate Kupiec POF test
def kupiec_pof_test(n, T, alpha=0.01):
    """
    n: Number of violations
    T: Total observations
    alpha: Significance level (default 0.01 for 99% VaR)
    """
    pi = n / T
    pi0 = alpha
    if pi in [0, 1]:
        return np.nan, np.nan  # Avoid log(0) or division by zero
    LR_pof = -2 * (np.log(((1 - pi0) ** (T - n)) * (pi0 ** n)) -
                   np.log(((1 - pi) ** (T - n)) * (pi ** n)))
    p_value = 1 - chi2.cdf(LR_pof, df=1)
    return LR_pof, p_value

# AIG data
T_aig = 752
aig_violations = {
    "Benchmark": 18,
    "Historical": 31,
    "GARCH": 11,
    "EGARCH": 9
}

# Chubb data
T_chubb = 752
chubb_violations = {
    "Benchmark": 11,
    "Historical": 7,
    "GARCH": 14,
    "EGARCH": 10
}

# Compute values
aig_results = {model: kupiec_pof_test(n, T_aig) for model, n in aig_violations.items()}
chubb_results = {model: kupiec_pof_test(n, T_chubb) for model, n in chubb_violations.items()}

print(aig_results, chubb_results)
