from data_types import DataType

class Row(dict):
    """Stores data for a single record (row) and has a unique id."""
    def __init__(self, data, id=None):
        super().__init__(data)
        self.id = id
        
    def __repr__(self):
        return f"<Row ID={self.id} Data={dict(self)}>"

class Column:
    """Describes a single table column, including type and constraints."""
    def __init__(self, name: str, data_type: DataType, nullable: bool, primary_key: bool, foreign_key=None):
        self.name = name
        self.data_type = data_type
        self.nullable = nullable
        self.primary_key = primary_key
        self.foreign_key = foreign_key

    def validate(self, value):
        """Validates the value against NULL constraints and data type."""
        if value is None:
            if not self.nullable:
                raise ValueError(f"Column '{self.name}' cannot be NULL.")
            return None
        return self.data_type.validate(value)


class Table:
    """Collection of columns and rows supporting basic CRUD and aggregation."""
    def __init__(self, name: str, columns: list):
        self.name = name
        self.columns = {c.name: c for c in columns} 
        self.rows = {} 
        self.next_id = 1

    def _validate_row(self, row_data: dict) -> dict:
        """Validates all row values against the column schema."""
        validated_data = {}
        for col_name, column in self.columns.items():
            value = row_data.get(col_name)
            validated_data[col_name] = column.validate(value)
        return validated_data

    def insert(self, row_data: dict) -> Row:
        """Creates a new row (Create) with PK uniqueness check."""
        validated_data = self._validate_row(row_data)

        pk_col_name = next((c.name for c in self.columns.values() if c.primary_key), None)
        if pk_col_name and validated_data.get(pk_col_name) is not None:
            if any(r.get(pk_col_name) == validated_data[pk_col_name] for r in self.rows.values()):
                raise ValueError(f"PK Error: Value '{validated_data[pk_col_name]}' already exists.")

        row = Row(validated_data, id=self.next_id)
        self.rows[self.next_id] = row
        self.next_id += 1
        return row

    def select_all(self) -> list[Row]:
        """Returns all rows in the table (Read)."""
        return list(self.rows.values())
    
    def count(self):
        """Returns the total number of rows."""
        return len(self.rows)
    
    def sum(self, col):
        """Calculates the sum of values in a numeric column, ignoring NULLs."""
        vals = [r.get(col) for r in self.rows.values() if col in r]
        valid_vals = [v for v in vals if isinstance(v, (int, float)) and v is not None] 
        return sum(valid_vals)
    
    def avg(self, col):
        """Calculates the average of values in a numeric column, ignoring NULLs."""
        vals = [r.get(col) for r in self.rows.values() if col in r]
        valid_vals = [v for v in vals if isinstance(v, (int, float)) and v is not None]
        return sum(valid_vals) / len(valid_vals) if valid_vals else 0


class SimpleQuery:
    """Performs queries with filtration (WHERE) and column selection."""
    def __init__(self, table: Table):
        self.table = table
        self.selected_columns = None
        self.filter_conditions = []

    def select(self, columns: list):
        """Specifies the columns to be returned."""
        self.selected_columns = columns
        return self 

    def where(self, column, operator, value):
        """Adds a simple filtration condition."""
        self.filter_conditions = [(column, operator, value)] 
        return self

    def execute(self):
        """Executes the query and returns filtered/selected rows."""
        filtered_rows = []
        
        for row in self.table.select_all():
            matches_all = True
            
            if self.filter_conditions:
                column, operator, value = self.filter_conditions[0]
                row_value = row.get(column)
                
                if operator == "==" and row_value != value: matches_all = False
                elif operator == ">" and not (row_value is not None and row_value > value): matches_all = False
                elif operator == "<" and not (row_value is not None and row_value < value): matches_all = False
            
            if matches_all:
                filtered_rows.append(row)
        
        results = []
        for row in filtered_rows:
            if self.selected_columns:
                new_row_data = {col: row[col] for col in self.selected_columns if col in row}
                results.append(Row(new_row_data))
            else:
                results.append(row)

        return results

class JoinedTable:
    """Represents a simplified result of an INNER JOIN operation (skeleton class)."""
    def __init__(self, left_table: Table, right_table: Table, on_columns: tuple):
        self.left = left_table
        self.right = right_table
        self.on_columns = on_columns
        
    def execute_join(self):
        """Returns an empty list as join logic is simplified/skipped."""
        return []