from abc import ABC, abstractmethod

class Container(ABC):
    """Абстрактний базовий клас для всіх контейнерів."""
    def __init__(self, id, weight):
        self._id = id 
        self._weight = weight

    @property
    def id(self):
        return self._id

    @property
    def weight(self):
        return self._weight

    @abstractmethod
    def consumption(self):
        """Повертає витрату палива, необхідну для перевезення контейнера."""
        pass

    def equals(self, other):
        if not isinstance(other, Container):
            return False
        return (type(self) == type(other) and
                self._id == other.id and
                self._weight == other.weight)

class BasicContainer(Container):
    """Контейнер, вага якого <= 3000. Витрата: 2.50 * вага."""
    _FUEL_RATE = 2.50
    def consumption(self):
        return self._weight * self._FUEL_RATE

class HeavyContainer(Container):
    """Контейнер, вага якого > 3000. Витрата: 3.00 * вага."""
    _FUEL_RATE = 3.00
    def consumption(self):
        return self._weight * self._FUEL_RATE

class RefrigeratedContainer(HeavyContainer):
    """Рефрижератор. Витрата: 5.00 * вага."""
    _FUEL_RATE = 5.00
    def consumption(self):
        return self._weight * self._FUEL_RATE

class LiquidContainer(HeavyContainer):
    """Контейнер для рідин. Витрата: 4.00 * вага."""
    _FUEL_RATE = 4.00
    def consumption(self):
        return self._weight * self._FUEL_RATE

def create_container_from_data(id, weight, type_char=None):
    """Фабрична функція для створення контейнера."""
    if type_char == 'R':
        return RefrigeratedContainer(id, weight)
    if type_char == 'L':
        return LiquidContainer(id, weight)
    if weight <= 3000:
        return BasicContainer(id, weight)
    else:
        return HeavyContainer(id, weight)