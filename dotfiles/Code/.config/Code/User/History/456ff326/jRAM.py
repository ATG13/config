"""Home loan calculator module.

Provides pure functions for standard and MaxGain-style home loan
amortization calculations. Uses only the Python standard library.

Version 1 -- constant od_balance.
Version 2 can replace the constant od_balance with a month-wise or
day-wise transaction stream by extending _build_maxgain_schedule.
"""

from typing import Any, Dict, List


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

    r = roi_annual / 12 / 100
    emi = principal * r * (1 + r) ** tenure_months / ((1 + r) ** tenure_months - 1)
    return round(emi, 2)


def _monthly_rate(roi_annual: float) -> float:
    return roi_annual / 12 / 100


def _round_2(value: float) -> float:
    return round(value, 2)


# ---------------------------------------------------------------------------
# Standard home loan
# ---------------------------------------------------------------------------

def _build_standard_schedule(
    principal: float,
    tenure_months: int,
    emi: float,
    rate: float,
) -> List[Dict[str, Any]]:
    """Build month-by-month amortisation schedule for a standard loan.

    Uses unrounded values for balance carry-over between months so that
    cumulative rounding error stays below 1 paisa.  The final month is
    adjusted so that ``closing_balance`` is exactly 0.
    """
    rows: List[Dict[str, Any]] = []
    balance = principal

    for month in range(1, tenure_months + 1):
        opening = balance
        interest_exact = opening * rate

        if month == tenure_months:
            # Force the loan to close to zero
            interest_comp = _round_2(interest_exact)
            principal_comp = _round_2(opening)
            closing = 0.0
            emi_actual = interest_comp + principal_comp
        else:
            interest_comp = interest_exact
            principal_comp = emi - interest_exact
            closing = opening - principal_comp
            emi_actual = emi

        rows.append({
            "month": month,
            "opening_balance": _round_2(opening),
            "emi": _round_2(emi_actual),
            "interest_component": _round_2(interest_comp),
            "principal_component": _round_2(principal_comp),
            "closing_balance": _round_2(closing),
        })

        balance = closing

    return rows


def standard_home_loan(
    principal: float,
    roi_annual: float,
    tenure_months: int,
) -> Dict[str, Any]:
    """Calculate a standard home-loan amortisation schedule.

    Args:
        principal: Initial loan principal (> 0).
        roi_annual: Annual rate of interest in percent (>= 0).
        tenure_months: Loan tenure in months (> 0).

    Returns:
        Dict with keys ``emi``, ``total_interest``, ``total_payment``
        and ``schedule`` (list of month dicts).
    """
    if principal <= 0:
        raise ValueError(f"principal must be positive, got {principal}")
    if tenure_months <= 0:
        raise ValueError(f"tenure_months must be positive, got {tenure_months}")
    if roi_annual < 0:
        raise ValueError(f"roi_annual must be non-negative, got {roi_annual}")

    emi = calculate_emi(principal, roi_annual, tenure_months)
    rate = _monthly_rate(roi_annual)
    schedule = _build_standard_schedule(principal, tenure_months, emi, rate)

    total_interest = _round_2(sum(r["interest_component"] for r in schedule))
    total_payment = _round_2(principal + total_interest)

    return {
        "emi": emi,
        "total_interest": total_interest,
        "total_payment": total_payment,
        "schedule": schedule,
    }


# ---------------------------------------------------------------------------
# MaxGain home loan (simplified, constant od_balance)
# ---------------------------------------------------------------------------

def _build_maxgain_schedule(
    principal: float,
    tenure_months: int,
    emi: float,
    rate: float,
    od_balance: float,
) -> List[Dict[str, Any]]:
    """Build amortisation schedule for MaxGain-style loan.

    .. note::

       This is a **simplified approximation** using a monthly offset
       model with a **constant** ``od_balance``.  Real MaxGain-style
       overdraft loans compute interest on daily balances and allow the
       surplus to vary throughout the month, which can produce different
       results from this monthly model.

    For version 2 the ``od_balance`` parameter can be replaced with a
    month-wise or day-wise transaction stream by passing a
    ``Callable[[int], float]`` or ``Sequence[float]`` instead.
    """
    rows: List[Dict[str, Any]] = []
    balance = principal
    settled = False

    for month in range(1, tenure_months + 1):
        if settled:
            rows.append(_zero_row(month))
            continue

        opening = balance
        effective = max(opening - od_balance, 0.0)
        interest_exact = effective * rate

        if month == tenure_months:
            interest_comp = _round_2(interest_exact)
            principal_comp = _round_2(opening)
            closing = 0.0
            emi_actual = interest_comp + principal_comp
        else:
            interest_comp = interest_exact
            principal_comp = emi - interest_exact
            closing_float = opening - principal_comp

            if closing_float <= 0:
                closing = 0.0
                settled = True
            else:
                closing = closing_float

            emi_actual = emi

        rows.append({
            "month": month,
            "opening_balance": _round_2(opening),
            "emi": _round_2(emi_actual),
            "interest_component": _round_2(interest_comp),
            "principal_component": _round_2(principal_comp),
            "closing_balance": _round_2(closing),
        })

        balance = closing

    return rows


def _zero_row(month: int) -> Dict[str, Any]:
    return {
        "month": month,
        "opening_balance": 0.0,
        "emi": 0.0,
        "interest_component": 0.0,
        "principal_component": 0.0,
        "closing_balance": 0.0,
    }


def maxgain_home_loan_simple(
    principal: float,
    roi_annual: float,
    tenure_months: int,
    od_balance: float,
) -> Dict[str, Any]:
    """Calculate a simplified MaxGain home-loan amortisation schedule.

    Uses the **same EMI** as the standard loan for the same
    ``(principal, roi_annual, tenure_months)`` but computes monthly
    interest on ``max(opening_balance - od_balance, 0)`` instead of the
    full opening balance.

    .. caution::

       This is a **simplified approximation** of a MaxGain-style
       overdraft loan.  Real MaxGain accounts typically compute
       interest daily on the net outstanding balance, and the surplus
       parked against the loan can change throughout the month.  The
       monthly offset model used here is intended for estimation and
       educational purposes only.

    Args:
        principal: Initial loan principal (> 0).
        roi_annual: Annual rate of interest in percent (>= 0).
        tenure_months: Loan tenure in months (> 0).
        od_balance: Constant overdraft / surplus balance (>= 0).

    Returns:
        Dict with keys ``emi``, ``total_interest``, ``total_payment``
        and ``schedule`` (list of month dicts).
    """
    if principal <= 0:
        raise ValueError(f"principal must be positive, got {principal}")
    if tenure_months <= 0:
        raise ValueError(f"tenure_months must be positive, got {tenure_months}")
    if roi_annual < 0:
        raise ValueError(f"roi_annual must be non-negative, got {roi_annual}")
    if od_balance < 0:
        raise ValueError(f"od_balance must be non-negative, got {od_balance}")

    emi = calculate_emi(principal, roi_annual, tenure_months)
    rate = _monthly_rate(roi_annual)
    schedule = _build_maxgain_schedule(principal, tenure_months, emi, rate, od_balance)

    total_interest = _round_2(sum(r["interest_component"] for r in schedule))
    total_payment = _round_2(principal + total_interest)

    return {
        "emi": emi,
        "total_interest": total_interest,
        "total_payment": total_payment,
        "schedule": schedule,
    }


# ---------------------------------------------------------------------------
# Demo (run with ``python -m loan_calculator``)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    std = standard_home_loan(5000000, 8.5, 60)
    print(
        f"Standard Loan: EMI={std['emi']}, "
        f"Interest={std['total_interest']}, "
        f"Payment={std['total_payment']}"
    )

    mg = maxgain_home_loan_simple(5000000, 8.5, 60, 10_00_000)
    print(
        f"MaxGain Loan:  EMI={mg['emi']}, "
        f"Interest={mg['total_interest']}, "
        f"Payment={mg['total_payment']}"
    )
