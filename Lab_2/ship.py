from abc import ABC, abstractmethod
from container import BasicContainer, HeavyContainer, RefrigeratedContainer, LiquidContainer
from port import Port 

class IShip(ABC):
    @abstractmethod
    def sailTo(self, port):
        pass

    @abstractmethod
    def reFuel(self, new_fuel):
        pass

    @abstractmethod
    def load(self, container):
        pass

    @abstractmethod
    def unLoad(self, container):
        pass

class Ship(IShip):
    """Клас Ship."""
    def __init__(self, id, current_port: Port, total_weight_capacity, max_all_containers,
                 max_heavy_containers, max_refrigerated_containers, 
                 max_liquid_containers, fuel_consumption_per_km, initial_fuel):
        
        self._id = id
        self._current_port = current_port 
        self._current_fuel = initial_fuel
        
        self._total_weight_capacity = total_weight_capacity
        self._max_all_containers = max_all_containers
        self._max_heavy_containers = max_heavy_containers
        self._max_refrigerated_containers = max_refrigerated_containers
        self._max_liquid_containers = max_liquid_containers
        self._fuel_consumption_per_km = fuel_consumption_per_km

        self._containers = [] 

        current_port.incomingShip(self) 

    @property
    def id(self):
        return self._id

    @property
    def current_fuel(self):
        return self._current_fuel
    
    @property
    def current_port(self): 
        return self._current_port

    def _get_current_weight(self):
        return sum(c.weight for c in self._containers)

    def _get_fuel_consumption(self, distance):
        """Розраховує загальну витрату палива (корабель + контейнери)."""
        total_consumption = distance * self._fuel_consumption_per_km
        container_consumption = sum(c.consumption() for c in self._containers)
        return total_consumption + container_consumption

    def sailTo(self, destination_port: Port):
        """Переміщує корабель до іншого порту."""
        if self._current_port == destination_port: return False

        distance = self._current_port.getDistance(destination_port)
        required_fuel = self._get_fuel_consumption(distance)

        if self._current_fuel >= required_fuel:
            self._current_port.outgoingShip(self)
            self._current_fuel -= required_fuel
            self._current_port = destination_port
            destination_port.incomingShip(self)
            return True
        else:
            return False

    def reFuel(self, new_fuel):
        """Додає паливо до корабля."""
        self._current_fuel += new_fuel

    def load(self, container):
        """Завантажує контейнер на корабель. ВИПРАВЛЕНА ЛОГІКА."""
        
        if self._get_current_weight() + container.weight > self._total_weight_capacity: 
            return False
        
        if len(self._containers) + 1 > self._max_all_containers: 
            return False
        
        current_heavy_count = sum(isinstance(c, HeavyContainer) for c in self._containers)
        current_refrigerated_count = sum(isinstance(c, RefrigeratedContainer) for c in self._containers)
        current_liquid_count = sum(isinstance(c, LiquidContainer) for c in self._containers)

        is_refrigerated = isinstance(container, RefrigeratedContainer)
        is_liquid = isinstance(container, LiquidContainer)
        is_heavy = isinstance(container, HeavyContainer)
        
        if is_heavy and current_heavy_count + 1 > self._max_heavy_containers: 
            return False
        
        if is_refrigerated and current_refrigerated_count + 1 > self._max_refrigerated_containers: 
            return False
        
        if is_liquid and current_liquid_count + 1 > self._max_liquid_containers: 
            return False

        if self._current_port.remove_container(container):
            self._containers.append(container)
            return True
        else:
            return False

    def unLoad(self, container):
        """Розвантажує контейнер з корабля."""
        if container in self._containers:
            self._containers.remove(container)
            self._current_port.add_container(container)
            return True
        else:
            return False
    
    def to_json_port_view(self):
        """Форматування для виводу в Port JSON."""
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
            
        return {
            f"ship_{self._id}": {
                "fuel_left": f"{self.current_fuel:.2f}",
                **container_ids_by_type
            }
        }