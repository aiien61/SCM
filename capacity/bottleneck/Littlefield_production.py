from dataclasses import dataclass
from enum import Enum
from typing import List, Dict
from collections import deque


class StationType(Enum):
    BOARD_STUFFING = "Board Stuffing"
    TESTING_1 = "Testing 1"
    TESTING_2 = "Testing 2"
    TUNING = "Tuning"

@dataclass
class StationConfig:
    setup_time: float  # hours/lot
    process_time: float  # hours/lot
    purchase_cost: float
    salvage_value: float
    capacity: int = 1  # number of machines

class ProductionStation:
    def __init__(self, station_type: StationType, config: StationConfig):
        self.station_type = station_type
        self.config = config
        self.queue = deque()
        self.machines: List[bool] = [False] * config.capacity

    @property
    def hourly_capacity(self) -> float:
        # calculate theoretical hourly capacity
        total_time_per_kit = self.config.process_time + (self.config.setup_time / 60)
        return self.config.capacity / total_time_per_kit
    
    @property
    def utilization(self) -> float:
        return len(m for m in self.machines if m) / len(self.machiens)

class MaterialInventory:
    def __init__(self):
        self.kit_cost = 10  # USD per kit
        self.setup_cost = 500  # USD
        self.lead_time = 4  # days
        self.reorder_point = 0
        self.order_quantity = 0
        self.current_stock = 0
        self.pending_orders = []

class ProductionSystem:
    def __init__(self):
        self.stations: Dict[StationType, ProductionStation] = {}
        self.inventory = MaterialInventory()
        self.initialize_stations()
    
    def initialize_stations(self):
        self.stations[StationType.BOARD_STUFFING] = ProductionStation(
            StationType.BOARD_STUFFING,
            StationConfig(
                setup_time=0.4,
                process_time=3.6/60,
                purchase_cost=100_000,
                salvage_value=40_000,
                capacity=1
            )
        )

        self.stations[StationType.TESTING_1] = ProductionStation(
            StationType.TESTING_1,
            StationConfig(
                setup_time=0.6,
                process_time=5.4/60,
                purchase_cost=200_000,
                salvage_value=80_000,
                capacity=1
            )
        )

        self.stations[StationType.TESTING_2] = ProductionStation(
            StationType.TESTING_2,
            StationConfig(
                setup_time=1.6,
                process_time=2.4/60,
                purchase_cost=200_000,
                salvage_value=80_000,
                capacity=1
            )
        )

        self.stations[StationType.TUNING] = ProductionStation(
            StationType.TUNING,
            StationConfig(
                setup_time=0.6,
                process_time=2.4/60,
                purchase_cost=130_000,
                salvage_value=80_000,
                capacity=1
            )
        )
    
    def analyze_capacity(self) -> Dict:
        results = {}
        for station_type, station in self.stations.items():
            total_time = station.config.process_time + (station.config.setup_time / 60)
            capacity = station.config.capacity * (1 / total_time)
            demand = 10
            utilization = demand / capacity

            results[station_type] = {
                "capacity": capacity,
                "demand": demand,
                "utilization": utilization,
                "is_bottleneck": utilization > 1.0
            }
        return results
    
class LittlefieldSimulation:
    def __init__(self):
        self.production_system = ProductionSystem()
        self.working_hours = 10
        self.lot_size = 60
        self.order_penalty = 1_500  # USD
        self.max_delivery_time = 5  # days
        self.bank_balance = 1_000_000  # USD
        self.interest_rate = 0.10  # 10% annual

    def run_capacity_analysis(self):
        print("\nLittlefield Production System Analysis")
        print("-" * 50)

        results = self.production_system.analyze_capacity()

        for station_type, result in results.items():
            print(f"\nStation {station_type.value}")
            print(f"Hourly Capacity: {result['capacity']:.2f} kits")
            print(f"Hourly Demand: {result['demand']} kits")
            print(f"Utilisation: {result['utilization']:.1%}")
            if result['is_bottleneck']:
                print("⚠️ This station is a bottleneck!")

def main():
    simulation = LittlefieldSimulation()
    simulation.run_capacity_analysis()

    # Example of strategies that can be implemented
    strategies = """
    Available Management Strategies:
    1. Capacity Management: Add/remove machines to match demand
    2. Inventory Management: Optimize material ordering and storage
    3. Lot Size Management: Adjust production batch sizes
    4. Order Management: Handle customer order policies
    5. Financial Management: Manage loans and capital
    6. Production Scheduling: Currently using FIFO
    """

    print(f"\n{strategies}")

if __name__ == "__main__":
    main()
