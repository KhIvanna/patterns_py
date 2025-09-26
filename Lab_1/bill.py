class Bill:
    """
    Class Bill represents the financial account of a customer.
    It stores the current debt and the maximum allowed limit.
    """

    def __init__(self, limiting_amount: float):
        """
        Initialize the bill with a limit and zero current debt.
        """
        self.limiting_amount = limiting_amount
        self.current_debt = 0.0

    def check(self, amount) -> bool:
        """
        Check if adding `amount` will exceed the limit.
        Returns True if allowed, False otherwise.
        """
        return (self.current_debt + amount) <= self.limiting_amount

    def add(self, amount):
        """Add a cost to the current debt."""
        if self.check(amount=amount):
            self.current_debt += amount
            print(f"Current debt has been increased to {self.current_debt}")

    def pay(self, amount):
        """Pay off part of the debt."""
        if amount > 0:
            self.current_debt -= amount
            if self.current_debt < 0:
                self.current_debt = 0.0

    def change_limit(self, amount):
        """Change the maximum allowed debt."""
        self.limiting_amount = amount
