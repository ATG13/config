from typing import Any, Dict, List

def _monthly_rate(roi_annual: float) -> float:
    return roi_annual / 12 / 100

def calculate_emi(principal: float, roi_annual: float, tenure_months: int) -> float:
    """Calculate the equated monthly installment.

    Args:
        principal: Initial loan principal (> 0).
        roi_annual: Annual rate of interest in percent (>= 0).
        tenure_months: Loan tenure in months (> 0).

    Returns:
        Monthly EMI amount rounded to 2 decimal places.
    """
    if principal <= 0:
        raise ValueError(f"principal must be positive, got {principal}")
    if tenure_months <= 0:
        raise ValueError(f"tenure_months must be positive, got {tenure_months}")
    if roi_annual < 0:
        raise ValueError(f"roi_annual must be non-negative, got {roi_annual}")

    if roi_annual == 0:
        return round(principal / tenure_months, 2)

    r = _monthly_rate(roi_annual)
    emi = principal * r * (1 + r) ** tenure_months / ((1 + r) ** tenure_months - 1)
    return round(emi, 2)

# Standard Home loan calculation

def standard_amount_repaid(principal:float, roi:float, tenure_months:int) -> float:
    """
    Calculate the Amount repaid in a standard home loan

    Args:
        principal: Initial loan principal (> 0).
        roi_annual: Annual rate of interest in percent (>= 0).
        tenure_months: Loan tenure in months (> 0).

    Returns:
        amount_repaid: Total amount repaid at the end of the home loan
    """
    emi = calculate_emi(principal,roi,tenure_months)

    amt_repaid = emi*tenure_months*12

    return round(amt_repaid,0)

print(standard_amount_repaid(50_00_000, 8.5, 60))