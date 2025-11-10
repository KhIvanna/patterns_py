from table import Table, Column
from data_types import TYPE_MAP, StringType

class Database:
    """The central manager of the DBMS, implemented as a Singleton pattern."""
    _instance = None
    _is_initialized = False

    def __new__(cls, *args, **kwargs):
        """Ensures only one instance of Database is created (Singleton)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name: str):
        if not Database._is_initialized:
            self.name = name
            self.tables = {} 
            Database._is_initialized = True

    def create_table_from_schema(self, table_name: str, schema: dict) -> Table:
        """
        Creates and registers a table based on a declarative schema (Factory Method).
        NOTE: This acts as the required Factory Method.
        """
        columns = []
        for col_schema in schema['columns']:
            type_name = col_schema['type'].lower()
            TypeClass = TYPE_MAP.get(type_name)
            
            if TypeClass is None:
                raise ValueError(f"Unknown data type: {col_schema['type']}")
            
            if TypeClass is StringType:
                 data_type = StringType(col_schema.get('max_length'))
            else:
                data_type = TypeClass()
            
            col = Column(
                name=col_schema['name'],
                data_type=data_type,
                nullable=col_schema.get('nullable', True),
                primary_key=col_schema.get('primary_key', False),
                foreign_key=col_schema.get('foreign_key', None) 
            )
            columns.append(col)
        
        table = Table(table_name, columns)
        self.tables[table_name] = table
        return table

    def get_table(self, name: str) -> Table:
        """Retrieves a table by name."""
        return self.tables.get(name)