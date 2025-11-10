import unittest
from database import Database
from table import Table, SimpleQuery
from data_types import IntegerType, StringType

class TestDBFramework(unittest.TestCase):
    """Test suite for the simplified DBMS framework."""

    @classmethod
    def setUpClass(cls):
        """Set up the environment: ensure clean Singleton state and create test table."""
        Database._instance = None 
        Database._is_initialized = False
        
        cls.db = Database("TestDB")

        test_schema = {
            "columns": [
                {"name": "tid", "type": "int", "nullable": False, "primary_key": True},
                {"name": "label", "type": "string", "nullable": False, "max_length": 10},
                {"name": "value", "type": "int", "nullable": True},
            ]
        }
        cls.test_table = cls.db.create_table_from_schema("test_data", test_schema)
        
        cls.test_table.insert({"tid": 1, "label": "A", "value": 10})
        cls.test_table.insert({"tid": 2, "label": "B", "value": 20})
        cls.test_table.insert({"tid": 3, "label": "C", "value": None}) # NULL value

    def test_database_is_singleton(self):
        """Checks if the Database class correctly implements the Singleton pattern."""
        db_new = Database("IgnoredName")
        self.assertIs(self.db, db_new, "Database instance should be the same (Singleton).")

    def test_primary_key_uniqueness(self):
        """Checks for Primary Key violation upon insertion of duplicate ID."""
        with self.assertRaisesRegex(ValueError, "PK Error: Value '1' already exists."):
            self.test_table.insert({"tid": 1, "label": "D", "value": 0})

    def test_not_nullable_violation(self):
        """Checks for NOT NULL constraint violation (Column 'label' is NOT NULL)."""
        with self.assertRaisesRegex(ValueError, "cannot be NULL"):
            self.test_table.insert({"tid": 4, "label": None, "value": 5})
            
    def test_data_type_violation(self):
        """Checks for data type mismatch (Expected int, got str)."""
        with self.assertRaisesRegex(ValueError, "Expected int"):
            self.test_table.insert({"tid": 4, "label": "D", "value": "text"})
            
    def test_max_length_violation(self):
        """Checks for StringType max_length constraint violation (max 10 chars)."""
        with self.assertRaisesRegex(ValueError, "exceeds max_length: 10"):
            self.test_table.insert({"tid": 4, "label": "TooLongLabel", "value": 1})

    def test_crud_and_simple_query(self):
        """Tests INSERT, COUNT, SELECT ALL, and SimpleQuery execution."""
        initial_count = self.test_table.count()
        new_id = 4
        
        self.test_table.insert({"tid": new_id, "label": "D", "value": 30})
        self.assertEqual(self.test_table.count(), initial_count + 1, "Count should increment after insert.")
        
        query = SimpleQuery(self.test_table)
        results = query.where("value", "==", 20).select(["label"]).execute()
        self.assertEqual(len(results), 1, "Query should return 1 row where value is 20.")
        self.assertEqual(results[0]['label'], "B")
        
        self.test_table.rows.pop(self.test_table.next_id - 1) 

    def test_aggregate_functions_count(self):
        """Tests the COUNT function."""
        self.assertEqual(self.test_table.count(), 3)

    def test_aggregate_functions_sum(self):
        """Tests the SUM function, ignoring NULL values (10 + 20 = 30)."""
        self.assertEqual(self.test_table.sum("value"), 30) 

    def test_aggregate_functions_avg(self):
        """Tests the AVG function, ignoring NULL values (30 / 2 = 15.0)."""
        self.assertEqual(self.test_table.avg("value"), 15.0)

if __name__ == '__main__':
    unittest.main()