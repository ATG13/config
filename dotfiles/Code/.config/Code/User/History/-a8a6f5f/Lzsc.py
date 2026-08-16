# Functions
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
    r = _monthly_rate(roi_annual)
    emi = principal * r * (1 + r) ** tenure_months / ((1 + r) ** tenure_months - 1)
    return emi

def standard_home_loan(principal: float, roi_annual: float, tenure_months: int) -> int:
    """Calculate the equated monthly installment.

    Args:
        principal: Initial loan principal (> 0).
        roi_annual: Annual rate of interest in percent (>= 0).
        tenure_months: Loan tenure in months (> 0).

    Returns:
        Amt_repaid: The total amount you pay (interest + principle)
    """
    emi = calculate_emi(principal, roi_annual, tenure_months)
    amt_repaid = int(round(emi*tenure_months,0))
    return amt_repaid

def maxgain_home_loan(principal: float, roi_annual: float, tenure_months: int, offset_balance: float) -> int:
    """Simulate a MaxGain home loan with a fixed offset account.

    Interest is charged on (outstanding − offset_balance) each month, so more
    of the fixed EMI goes toward principal, paying off the loan early.

    Args:
        principal: Initial loan principal (> 0).
        roi_annual: Annual rate of interest in percent (>= 0).
        tenure_months: Loan tenure in months (> 0).
        offset_balance: Fixed balance in the offset account (>= 0).

    Returns:
        total_paid: Amount + Interest with OD balance
    """
    r = _monthly_rate(roi_annual)
    emi = calculate_emi(principal, roi_annual, tenure_months)

    outstanding = float(principal)
    total_interest = 0.0
    months_elapsed = 0

    while outstanding > 0.01:
        effective = max(0.0, outstanding - offset_balance)
        interest = effective * r

        if interest >= emi:
            print("Maxgain home loan")
            print(f"EMI: \u20b9{emi:,}")
            print("Loan will never be paid off \u2014 interest exceeds EMI.")
            return

        principal_repaid = emi - interest

        if principal_repaid >= outstanding:
            total_interest += interest
            outstanding = 0.0
        else:
            outstanding -= principal_repaid
            total_interest += interest

        months_elapsed += 1

        if months_elapsed > tenure_months * 2:
            break

    total_paid = principal + total_interest
    standard_total = standard_home_loan(principal, roi_annual, tenure_months)
    standard_interest = standard_total - principal
    interest_saved = standard_interest - round(total_interest)
    months_saved = tenure_months - months_elapsed

    # print("Maxgain home loan")
    # print(f"EMI: \u20b9{emi:,}")
    # print(f"Loan paid off in {months_elapsed} months ({months_saved} months early)")
    # print(f"Total repaid: \u20b9{round(total_paid):,}")
    # print(f"Total interest paid: \u20b9{round(total_interest):,}")
    # print(f"Interest saved vs standard: \u20b9{interest_saved:,}")
    return int(total_paid)