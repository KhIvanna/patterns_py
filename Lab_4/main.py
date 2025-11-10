from database import Database
from table import SimpleQuery, JoinedTable 
from datetime import datetime

db = Database("MySimpleDB") 
db_check = Database("Ignored")

print(f"Database instance check (Singleton): {db is db_check}")

users_schema = {
    "columns": [
        {"name": "user_id", "type": "int", "nullable": False, "primary_key": True},
        {"name": "name", "type": "string", "nullable": False, "max_length": 50},
        {"name": "is_active", "type": "bool", "nullable": True},
        {"name": "created_at", "type": "date", "nullable": False},
    ]
}
users = db.create_table_from_schema("users", users_schema)

orders_schema = {
    "columns": [
        {"name": "order_id", "type": "int", "nullable": False, "primary_key": True},
        {"name": "user_id", "type": "int", "nullable": False, "foreign_key": ("users", "user_id")}, # FK is for structure only
        {"name": "amount", "type": "int", "nullable": False},
    ]
}
orders = db.create_table_from_schema("orders", orders_schema)

print("\n--- Inserting Data ---")
users.insert({"user_id": 1, "name": "Alice", "is_active": True, "created_at": "2024-01-01"})
users.insert({"user_id": 2, "name": "Bob", "is_active": False, "created_at": datetime.now()})
orders.insert({"order_id": 101, "user_id": 1, "amount": 150})
orders.insert({"order_id": 102, "user_id": 2, "amount": 250})

print(f"\nTotal users: {users.count()}")

print("\n--- SimpleQuery (WHERE & SELECT) ---")
query = SimpleQuery(users)
results = query.where("name", "==", "Bob").select(["user_id", "is_active"]).execute()

for row in results:
    print(row)

print(f"Total order amount: {orders.sum('amount')}")