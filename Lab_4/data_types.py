from abc import ABC, abstractmethod
from datetime import datetime

class DataType(ABC):
    """Base class for all data types in the DBMS (Pattern: Abstract Class)."""
    @abstractmethod
    def validate(self, value):
        """Checks if the value conforms to the data type and returns it (possibly converted)."""
        pass

class IntegerType(DataType):
    """Data type for integer numbers."""
    def validate(self, value):
        if not isinstance(value, int):
            raise ValueError(f"Expected int, got {type(value).__name__}")
        return value

class StringType(DataType):
    """Data type for strings with optional max_length constraint."""
    def __init__(self, max_length=None):
        self.max_length = max_length
        
    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError(f"Expected str, got {type(value).__name__}")
        if self.max_length is not None and len(value) > self.max_length:
            raise ValueError(f"String length exceeds max_length: {self.max_length}")
        return value

class BooleanType(DataType):
    """Data type for boolean values."""
    def validate(self, value):
        if not isinstance(value, bool):
            raise ValueError(f"Expected bool, got {type(value).__name__}")
        return value

class DateType(DataType):
    """Data type for date and time objects."""
    def validate(self, value):
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("Date string must be in ISO format (YYYY-MM-DD...).")
        raise ValueError(f"Expected datetime or str, got {type(value).__name__}")

TYPE_MAP = {
    'int': IntegerType,
    'string': StringType,
    'bool': BooleanType,
    'date': DateType
}