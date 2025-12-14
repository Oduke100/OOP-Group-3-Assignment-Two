import random
import time
import pandas as pd
from IPython.display import display, clear_output

# ----------------------
# Classes
# ----------------------
class BaseStation:
    def __init__(self, bs_id, location, capacity=5):
        self.bs_id = bs_id
        self.location = location
        self.capacity = capacity
        self.connected_devices = []

class SmartPhone:
    def __init__(self, device_id):
        self.device_id = device_id
        self.location = None
    def connect(self, bs):
        bs.connected_devices.append(self)

class Passenger:
    def __init__(self, passenger_id, device, destination):
        self.passenger_id = passenger_id
        self.device = device
        self.destination = destination

class Driver:
    def __init__(self, driver_id, name, location):
        self.driver_id = driver_id
        self.name = name
        self.location = location
        self.available = True
        self.current_passenger = None

class NetworkSimulator:
    def __init__(self):
        self.base_stations = []
        self.devices = []
        self.passengers = []
        self.drivers = []

    def add_base_station(self, bs):
        self.base_stations.append(bs)
    def add_device(self, device):
        self.devices.append(device)
    def add_passenger(self, passenger):
        self.passengers.append(passenger)
    def add_driver(self, driver):
        self.drivers.append(driver)
    def assign_drivers(self):
        # simple random assignment for demo
        for passenger in self.passengers:
            available_drivers = [d for d in self.drivers if d.available]
            if available_drivers:
                driver = random.choice(available_drivers)
                driver.current_passenger = passenger.passenger_id
                driver.available = False

# ----------------------
# Simulation setup
# ----------------------
LOCATIONS = ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Shakahola"]

# Base stations
BASE_STATIONS = [BaseStation(f"BS-{i+1:03}", loc) for i, loc in enumerate(LOCATIONS)]

# Network
NETWORK = NetworkSimulator()
for bs in BASE_STATIONS:
    NETWORK.add_base_station(bs)

# Devices and passengers
for i in range(10):
    device = SmartPhone(f"D-{1000+i}")
    NETWORK.add_device(device)
    passenger = Passenger(f"P-{300+i}", device, random.choice(LOCATIONS))
    NETWORK.add_passenger(passenger)

# Drivers
driver_names = ["Alice", "Bob", "Charlie", "David", "Eva"]
for i in range(5):
    driver = Driver(f"DR-{200+i}", driver_names[i], random.choice(LOCATIONS))
    NETWORK.add_driver(driver)

# ----------------------
# Simulation loop
# ----------------------
def get_bs_identifier(bs):
    return getattr(bs, "bs_id", str(bs))

try:
    while True:
        clear_output(wait=True)

        # Randomize passenger locations and destinations
        for passenger in NETWORK.passengers:
            passenger.device.location = random.choice(LOCATIONS)
            passenger.destination = random.choice([loc for loc in LOCATIONS if loc != passenger.device.location])

        # Randomize driver locations
        for driver in NETWORK.drivers:
            if driver.available:
                driver.location = random.choice(LOCATIONS)

        # Reset base station connections and reconnect devices
        for bs in NETWORK.base_stations:
            bs.connected_devices.clear()
        for device in NETWORK.devices:
            candidates = [bs for bs in NETWORK.base_stations if bs.location == device.location]
            if candidates:
                bs = random.choice(candidates)
                device.connect(bs)

        # Assign drivers to passengers
        NETWORK.assign_drivers()

        # Build tables
        bs_data = [{"BaseStation": get_bs_identifier(bs),
                    "Location": bs.location,
                    "Connected Devices": len(bs.connected_devices)}
                   for bs in NETWORK.base_stations]

        drivers_data = [{"Driver": d.name,
                         "Location": d.location,
                         "Status": "Busy" if d.current_passenger else "Available"}
                        for d in NETWORK.drivers]

        passengers_data = [{"Passenger": p.passenger_id,
                            "Location": p.device.location,
                            "Destination": p.destination}
                           for p in NETWORK.passengers]

        # Display tables
        display(pd.DataFrame(bs_data))
        display(pd.DataFrame(drivers_data))
        display(pd.DataFrame(passengers_data))

        time.sleep(2)

except KeyboardInterrupt:
    print("\nSimulation stopped manually.")
