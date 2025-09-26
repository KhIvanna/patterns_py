from customer import Customer
from operator_ import Operator

class Main:
    """
    Main class runs the simulation of customers and operators.
    """

    def __init__(self):
        self.customers = []
        self.operators = []

    def create_operator(self, ID, talking_charge, message_cost, network_charge, discount_rate):
        operator = Operator(ID, talking_charge, message_cost, network_charge, discount_rate)
        self.operators.append(operator)
        print(f"Created operator with ID {operator.ID}.")

    def create_customer(self, ID, name, age):
        customer = Customer(ID, name, age)
        self.customers.append(customer)
        print(f"Created customer with ID {customer.ID}.")

    def run_simulation(self):
        print("--- Creating operators ---")
        self.create_operator(0, 0.5, 0.1, 0.2, 0.1)
        self.create_operator(1, 0.6, 0.15, 0.3, 0.2)

        print("\n--- Creating customers ---")
        self.create_customer(0, "Ivan", 25)
        self.create_customer(1, "Maria", 17)
        self.create_customer(2, "Petro", 70)

        ivan = self.customers[0]
        maria = self.customers[1]
        petro = self.customers[2]

        # Connect Ivan to both operators
        ivan.set_operator(self.operators[0])
        ivan.set_operator(self.operators[1])

        # Other customers connect
        maria.set_operator(self.operators[0])
        petro.set_operator(self.operators[1])

        print("\n--- Ivan selects an operator for a call ---")
        print(f"Available operators for Ivan: {list(ivan.operators.keys())}")

        # Ivan calls Maria using operator ID=0
        print("Ivan calls Maria using operator ID=0.")
        ivan.talk(10, maria, 0)
        
        # Ivan calls Petro using operator ID=1
        print("Ivan calls Petro using operator ID=1.")
        ivan.talk(5, petro, 1)

        print("\n--- Customers messaging ---")
        ivan.message(10, maria, 0)
        ivan.message(10, petro, 0)

        print("\n--- Customers using internet ---")
        ivan.connection(50, 0)
        ivan.connection(1000, 0)

        print("\n--- Customers paying bills ---")
        ivan.pay_bill(10)

        print("\n--- Customers changing bill limit ---")
        ivan.change_bill_limit(1000, 0)
        ivan.connection(50, 0)


if __name__ == "__main__":
    app = Main()
    app.run_simulation()