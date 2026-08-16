from dataclasses import dataclass
from typing import Optional


@dataclass
class Customer:
    customer_id: int
    name: str
    age: int
    city: str
    email: str

    # Optional: store loan preferences
    loan_amount: Optional[float] = None       # principal
    annual_interest_rate: Optional[float] = None  # in %
    tenure_years: Optional[int] = None        # in years

class HomeLoan:
    def __init__(self, customer: Customer, loan_amount: float,
                 annual_interest_rate: float, tenure_years: int) -> None:
        self.customer = customer
        self.loan_amount = loan_amount
        self.annual_interest_rate = annual_interest_rate
        self.tenure_years = tenure_years

    @property
    def tenure_months(self) -> int:
        return self.tenure_years * 12

    @property
    def monthly_interest_rate(self) -> float:
        # Annual rate given as %, convert to monthly decimal
        return self.annual_interest_rate / (12 * 100)

    def calculate_emi(self) -> float:
        """
        Calculate the Equated Monthly Instalment (EMI).

        Formula:
        EMI = [P x R x (1+R)^N] / [(1+R)^N - 1]
        P = principal (loan_amount)
        R = monthly interest rate (decimal)
        N = tenure in months
        """
        P = self.loan_amount
        R = self.monthly_interest_rate
        N = self.tenure_months

        if R == 0:  # edge case: 0% interest
            return P / N

        factor = (1 + R) ** N
        emi = P * R * factor / (factor - 1)
        return emi

    def total_payment(self) -> float:
        return self.calculate_emi() * self.tenure_months

    def total_interest(self) -> float:
        return self.total_payment() - self.loan_amount

    def summary(self) -> dict:
        emi = self.calculate_emi()
        return {
            "customer_name": self.customer.name,
            "loan_amount": self.loan_amount,
            "annual_interest_rate": self.annual_interest_rate,
            "tenure_years": self.tenure_years,
            "tenure_months": self.tenure_months,
            "monthly_emi": round(emi, 2),
            "total_payment": round(self.total_payment(), 2),
            "total_interest": round(self.total_interest(), 2),
        }


# Example usage / quick test
if __name__ == "__main__":
    # Create a customer
    cust = Customer(
        customer_id=1,
        name="Rahul Sharma",
        age=32,
        city="Bengaluru",
        email="rahul@example.com"
    )

    # Create a home loan for this customer
    loan = HomeLoan(
        customer=cust,
        loan_amount=5_000_000,       # 50 lakh
        annual_interest_rate=8.5,    # 8.5% p.a.
        tenure_years=20              # 20 years
    )

    info = loan.summary()
    print(f"Customer: {info['customer_name']}")
    print(f"Loan amount: {info['loan_amount']}")
    print(f"Annual interest rate: {info['annual_interest_rate']}%")
    print(f"Tenure: {info['tenure_years']} years ({info['tenure_months']} months)")
    print(f"Monthly EMI: {info['monthly_emi']}")
    print(f"Total payment: {info['total_payment']}")
    print(f"Total interest: {info['total_interest']}")
