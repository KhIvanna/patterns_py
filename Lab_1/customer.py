from __future__ import annotations
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from operator_ import Operator

class Customer:
    """
    Class Customer represents a customer who can talk, send messages, and use internet.
    """

    def __init__(self, ID, name, age):
        """
        Initialize a customer with ID, name, age, operator, bill, and limit.
        """
        self.ID = ID
        self.name = name
        self.age = age
        self.operators: Dict[int, Operator] = {}

    def talk(self, minutes: int, other: 'Customer', operator_id: int):
        """Talk to another customer."""
        operator: Operator = self.operators.get(operator_id)
        if operator:
            cost = operator.calculate_talking_cost(minutes, self)
            print(f"Customer {self.name} is talking to {other.name}. Cost = {cost}")


    def message(self, quantity, other: 'Customer', operator_id: int) -> None:
        """Send messages to another customer."""
        operator: Operator = self.operators.get(operator_id)
        if operator:
            cost = operator.calculate_message_cost(quantity, self, other)
            print(f"Customer {self.name} sent {quantity} messages to {other.name}. Cost: {cost:.2f} UAH.")
        else:
            print(f"No such operator with ID = {operator_id}")

    def connection(self, amount: float, operator_id: int) -> None:
        """Use internet (MB)."""
        operator: Operator = self.operators.get(operator_id)
        if operator:
            cost = operator.calculate_network_cost(amount, self)
            print(f"Customer {self.name} used {amount:.2f} MB of internet. Cost: {cost:.2f} UAH.")
        else:
            print(f"No such operator with ID = {operator_id}")


    def pay_bill(self, amount):
        if hasattr(self, 'operator'):
            self.operator.bills[self.ID].pay(amount)
            print(f"Customer {self.name} paid {amount:.2f} UAH. Current debt: {self.operator.bills[self.ID].current_debt:.2f} UAH.")
        else:
            print(f"{self.name} has no operator assigned yet.")


    def set_operator(self, new_operator: Operator):
        """Assigns a new operator to the customer, adding it to the list of available ones."""
        new_operator.assign(self)
        self.operators[new_operator.ID] = new_operator
        self.operator = new_operator
        print(f"Customer {self.name} assigned operator {new_operator.ID}.")

    def change_bill_limit(self, new_limit, operator_id: int):
        """Change bill limit."""
        operator: Operator = self.operators.get(operator_id)
        if operator:
            operator.bills[self.ID].change_limit(new_limit)
            print(f"Customer {self.name} changed bill limit to {new_limit:.2f} UAH.")
        else:
            print(f"No such operator with ID = {operator_id}")
