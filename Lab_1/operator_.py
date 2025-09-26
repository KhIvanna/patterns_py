from __future__ import annotations
from typing import Dict, TYPE_CHECKING
from bill import Bill  

if TYPE_CHECKING:
    from customer import Customer

class Operator:
    """
    Class Operator represents a mobile operator with costs for talk, message, and internet.
    """

    LIMITING_AMOUNT: float = 300.0

    def __init__(self, ID, talking_charge, message_cost, network_charge, discount_rate):
        """
        Initialize operator with given charges and discount rate.
        """
        self.ID = ID
        self.talking_charge = talking_charge
        self.message_cost = message_cost
        self.network_charge = network_charge
        self.discount_rate = discount_rate

        self.bills: Dict[int, Bill] = {}

    def assign(self, customer: Customer) -> None:
        self.bills[customer.ID] = Bill(limiting_amount = self.LIMITING_AMOUNT)

    def _calculate_discounted_cost(self, original_cost: float, customer: Customer) -> float:
        """
        A private helper method to apply a discount based on customer's age.
        """
        if customer.age < 18 or customer.age > 65:
            return original_cost * (1 - self.discount_rate)
        return original_cost

    def calculate_talking_cost(self, minutes: int, customer: Customer):
        """
        Calculate cost of talking.
        Discount applies if customer is under 18 or over 65.
        """
        cost = minutes * self.talking_charge
        cost = self._calculate_discounted_cost(cost, customer)
        self.bills[customer.ID].add(amount=cost)
        return round(cost, 2)

    def calculate_message_cost(self, quantity, sender, receiver):
        """
        Calculate cost of sending messages.
        Discount applies if both customers use the same operator.
        """
        cost = quantity * self.message_cost
        if sender.operator.ID == receiver.operator.ID:
            cost *= (1 - self.discount_rate)
        self.bills[sender.ID].add(amount=cost)
        return round(cost, 2)

    def calculate_network_cost(self, amount, customer: Customer):
        """Calculate internet cost (straightforward: MB * network_charge)."""
        cost = amount * self.network_charge
        self.bills[customer.ID].add(amount=cost)
        return round(cost, 2)