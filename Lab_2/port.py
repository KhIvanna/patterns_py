from abc import ABC, abstractmethod
from math import radians, sin, cos, sqrt, atan2
from container import BasicContainer, HeavyContainer, RefrigeratedContainer, LiquidContainer 

class IPort(ABC):
    @abstractmethod
    def incomingShip(self, ship):
        pass

    @abstractmethod
    def outgoingShip(self, ship):
        pass

class Port(IPort):
    """Клас Port."""
    def __init__(self, id, latitude, longitude):
        self._id = id
        self._latitude = latitude
        self._longitude = longitude
        self._containers = []        
        self._ship_current = []      

    @property
    def id(self):
        return self._id

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    def getDistance(self, other):
        """Розраховує відстань між двома портами (Формула Гаверсіна)."""
        R = 6371 
        lat1, lon1 = radians(self._latitude), radians(self._longitude)
        lat2, lon2 = radians(other.latitude), radians(other.longitude)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    def incomingShip(self, ship):
        """Додає корабель до поточних кораблів."""
        if ship not in self._ship_current:
            self._ship_current.append(ship)
            return True
        return False

    def outgoingShip(self, ship):
        """Видаляє корабель з поточних."""
        if ship in self._ship_current:
            self._ship_current.remove(ship)
            return True
        return False

    def add_container(self, container):
        """Додає контейнер до порту."""
        self._containers.append(container)

    def remove_container(self, container):
        """Видаляє контейнер з порту."""
        if container in self._containers:
            self._containers.remove(container)
            return True
        return False
    
    def to_json(self, all_ships):
        """Формує вихідний JSON-об'єкт для порту."""
        
        container_ids_by_type = {
            "basic_container": [],
            "heavy_container": [],
            "refrigerated_container": [],
            "liquid_container": []
        }
        
        for cont in sorted(self._containers, key=lambda c: c.id):
            if isinstance(cont, RefrigeratedContainer):
                container_ids_by_type["refrigerated_container"].append(cont.id)
            elif isinstance(cont, LiquidContainer):
                container_ids_by_type["liquid_container"].append(cont.id)
            elif isinstance(cont, BasicContainer):
                container_ids_by_type["basic_container"].append(cont.id)
            elif isinstance(cont, HeavyContainer):
                container_ids_by_type["heavy_container"].append(cont.id)

        ship_list = []
        for ship in sorted(self._ship_current, key=lambda s: s.id):
             ship_list.append(ship.to_json_port_view()) 

        return {
            "Port ID": self.id,
            "lat": f"{self.latitude:.2f}",
            "lon": f"{self.longitude:.2f}",
            "basic_container": container_ids_by_type["basic_container"],
            "heavy_container": container_ids_by_type["heavy_container"],
            "refrigerated_container": container_ids_by_type["refrigerated_container"],
            "liquid_container": container_ids_by_type["liquid_container"],
            "ships": ship_list
        }