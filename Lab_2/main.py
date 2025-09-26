import json
from id_generator import IDGenerator
from container import create_container_from_data
from port import Port 
from ship import Ship 

class Main:
    """Головний клас, що керує симуляцією, читає/пише JSON та обробляє команди."""
    def __init__(self, input_filename="input.json", output_filename="output.json"):
        self.ports = {}  
        self.ships = {}  
        self.containers = {} 
        self.input_filename = input_filename
        self.output_filename = output_filename
        IDGenerator.reset() 

    def _get_item(self, item_dict, item_id, item_type):
        """Допоміжна функція для отримання об'єкта за ID та перевірки існування."""
        try:
            item_id = int(item_id) 
            item = item_dict.get(item_id)
            if item is None:
                print(f"Error: {item_type} with ID {item_id} not found.")
            return item
        except (ValueError, TypeError):
             print(f"Error: Invalid ID format or type provided.")
             return None

    def process_command(self, command):
        """Обробляє одну команду з вхідного JSON."""
        action = command.get("action")
        data = command.get("data", {})
        
        print(f"\n--- Processing: {action} ---") 

        if action == "CreateContainer":
            weight = data.get("weight")
            type_char = data.get("type_char")
            port_id = data.get("port_id")
            
            if weight is None or weight <= 0: 
                print("Error: Invalid or missing 'weight'.")
                return

            container_id = IDGenerator.get_next_id()
            container = create_container_from_data(container_id, weight, type_char)
            self.containers[container_id] = container
            
            msg = f"Created {type(container).__name__} ID {container_id}, Weight {weight}."
            if port_id is not None:
                initial_port = self._get_item(self.ports, port_id, "Port")
                if initial_port:
                    initial_port.add_container(container)
                    msg += f" Placed in Port {port_id}."
                else:
                    msg += f" (Port {port_id} not found, container created but unattached)."
            print(msg)
                
        elif action == "CreateShip":
            port_id = data.get("port_id")
            current_port = self._get_item(self.ports, port_id, "Port")
            if current_port is None: return

            ship_params = {
                "total_weight_capacity": data.get("total_weight_capacity"),
                "max_all_containers": data.get("max_all_containers"),
                "max_heavy_containers": data.get("max_heavy_containers"),
                "max_refrigerated_containers": data.get("max_refrigerated_containers"),
                "max_liquid_containers": data.get("max_liquid_containers"),
                "fuel_consumption_per_km": data.get("fuel_consumption_per_km"),
                "initial_fuel": data.get("initial_fuel", 0.0)
            }
            
            ship_id = IDGenerator.get_next_id()
            ship = Ship(ship_id, current_port, **ship_params)
            self.ships[ship_id] = ship
            print(f"Created Ship {ship_id} at Port {port_id} (Fuel: {ship.current_fuel:.2f}).")

        elif action == "CreatePort":
            port_id = IDGenerator.get_next_id()
            latitude = data.get("latitude")
            longitude = data.get("longitude")

            port = Port(port_id, latitude, longitude)
            self.ports[port_id] = port
            print(f"Created Port {port_id} at ({latitude:.2f}, {longitude:.2f}).")
            
        elif action == "LoadContainer":
            ship_id = data.get("ship_id")
            container_id = data.get("container_id")

            ship = self._get_item(self.ships, ship_id, "Ship")
            container = self._get_item(self.containers, container_id, "Container")

            if ship and container:
                if ship.load(container):
                    print(f"SUCCESS: Ship {ship_id} loaded Container {container_id}.")
                else:
                    print(f"FAILED: Ship {ship_id} failed to load Container {container_id} (check port presence, capacity, or type limits).")

        elif action == "UnloadContainer":
            ship_id = data.get("ship_id")
            container_id = data.get("container_id")

            ship = self._get_item(self.ships, ship_id, "Ship")
            container = self._get_item(self.containers, container_id, "Container")

            if ship and container:
                if ship.unLoad(container):
                    print(f"SUCCESS: Ship {ship_id} unloaded Container {container_id} at Port {ship.current_port.id}.")
                else:
                    print(f"FAILED: Ship {ship_id} failed to unload Container {container_id} (not on ship).")
        
        elif action == "SailTo":
            ship_id = data.get("ship_id")
            destination_port_id = data.get("destination_port_id")

            ship = self._get_item(self.ships, ship_id, "Ship")
            destination_port = self._get_item(self.ports, destination_port_id, "Port")

            if ship and destination_port:
                if ship.sailTo(destination_port):
                    print(f"SUCCESS: Ship {ship_id} sailed to Port {destination_port.id}. Fuel left: {ship.current_fuel:.2f}.")
                else:
                    print(f"FAILED: Ship {ship_id} could not sail to Port {destination_port.id} (not enough fuel).")
        
        elif action == "RefuelShip":
            ship_id = data.get("ship_id")
            amount = data.get("amount")

            ship = self._get_item(self.ships, ship_id, "Ship")

            if ship and amount is not None and amount > 0:
                ship.reFuel(amount)
                print(f"SUCCESS: Ship {ship_id} refueled by {amount:.2f}. New fuel: {ship.current_fuel:.2f}.")
            else:
                 print(f"FAILED: Ship {ship_id} could not be refueled (invalid amount).")

    def run_simulation(self):
        """Зчитує JSON, виконує команди та записує результат."""
        try:
            with open(self.input_filename, 'r') as f:
                commands = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"FATAL ERROR: Could not read input file. {e}")
            return

        for command in commands:
            self.process_command(command)

        self.generate_output()

    def generate_output(self):
        """Формує кінцевий JSON-файл."""
        output_data = []
        
        sorted_ports = sorted(self.ports.values(), key=lambda p: p.id)

        for port in sorted_ports:
            port_json = port.to_json(self.ships)
            output_data.append({f"Port {port.id}": port_json})

        # Запис у файл
        try:
            with open(self.output_filename, 'w') as f:
                json.dump(output_data, f, indent=4)
            print(f"\nСимуляція завершена. Результат збережено у '{self.output_filename}'.")
        except Exception as e:
            print(f"ERROR writing output file: {e}")

if __name__ == "__main__":
    
    IDGenerator.reset() 
    
    test_commands = [
        {"action": "CreatePort", "data": {"latitude": 40.71, "longitude": -74.01}}, 
        {"action": "CreatePort", "data": {"latitude": 40.05, "longitude": -95.24}},
        
        {"action": "CreateContainer", "data": {"weight": 2500, "type_char": None, "port_id": 1}},
        {"action": "CreateContainer", "data": {"weight": 5000, "type_char": None, "port_id": 1}},
        {"action": "CreateContainer", "data": {"weight": 1000, "type_char": "R", "port_id": 1}}, 
        {"action": "CreateContainer", "data": {"weight": 6000, "type_char": "L", "port_id": 1}}, 
        
        {"action": "CreateShip", "data": { 
            "port_id": 1, "total_weight_capacity": 20000, "max_all_containers": 10,
            "max_heavy_containers": 5, "max_refrigerated_containers": 2, "max_liquid_containers": 2,
            "fuel_consumption_per_km": 0.5, "initial_fuel": 200000.0
        }}, 
        
        {"action": "LoadContainer", "data": {"ship_id": 7, "container_id": 3}}, 
        {"action": "LoadContainer", "data": {"ship_id": 7, "container_id": 5}}, 
        {"action": "LoadContainer", "data": {"ship_id": 7, "container_id": 6}}, 
        
        {"action": "RefuelShip", "data": {"ship_id": 7, "amount": 500.0}},
        {"action": "SailTo", "data": {"ship_id": 7, "destination_port_id": 2}},
        
        {"action": "UnloadContainer", "data": {"ship_id": 7, "container_id": 3}}, 
        {"action": "UnloadContainer", "data": {"ship_id": 7, "container_id": 5}},
        {"action": "UnloadContainer", "data": {"ship_id": 7, "container_id": 6}},
    ]

    with open("input.json", 'w') as f:
        json.dump(test_commands, f, indent=4)

    simulation = Main()
    simulation.run_simulation()