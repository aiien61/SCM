from abc import ABC, abstractmethod
from typing import List
import numpy as np

class WorkCenter:
    def __init__(self, machines: int, machine_hours_per_day: int, machine_days_per_week: int, workers: int, worker_hours_per_day: int):
        self.machines = machines
        self.machine_hours_per_day = machine_hours_per_day
        self.machine_days_per_week = machine_days_per_week
        self.machine_available_time = self.calculate_machine_available_time()

        self.workers = workers
        self.worker_hours_per_day = worker_hours_per_day
        self.worker_available_time = self.calculate_worker_available_time()

    def calculate_machine_available_time(self):
        """Calculate total available time of machines"""
        return self.machines * self.machine_hours_per_day * self.machine_days_per_week
    
    def calculate_worker_available_time(self):
        """Calculate total available time of workers"""
        return self.workers * self.worker_hours_per_day * self.machine_days_per_week


class CapacityStrategy(ABC):
    @abstractmethod
    def calculate_capacity(slef):
        raise NotImplementedError
    

class RatedCapacityStrategy(CapacityStrategy):
    def calculate_capacity(self, machine_time: int, worker_time: int, utilization: float, efficiency: float) -> float:
        """Calculate rated capacity, including both machinery and workforce"""
        total_available_time = machine_time + worker_time
        return total_available_time * utilization * efficiency


class MeasuredCapacityStrategy(CapacityStrategy):
    def calculate_capacity(self, historical_data: List[int]):
        """Calculate measured capacity based on historical data"""
        return np.mean(historical_data)


class CapacityCalculator:
    def __init__(self, strategy: CapacityStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: CapacityStrategy):
        self.strategy = strategy

    def calculate(self, *args, **kwargs) -> float:
        return self.strategy.calculate_capacity(*args, **kwargs)


if __name__ == "__main__":
    # Define a work centre, including machinery and workforce
    work_center = WorkCenter(machines=4, machine_hours_per_day=8, machine_days_per_week=5, workers=3, worker_hours_per_day=7)

    # Calculate rated capacity
    rated_strategy: CapacityStrategy = RatedCapacityStrategy()
    calculator: CapacityCalculator = CapacityCalculator(strategy=rated_strategy)
    rated_capacity: float = calculator.calculate(
        machine_time=work_center.machine_available_time,
        worker_time=work_center.worker_available_time,
        utilization=0.85,
        efficiency=1.1
    )
    print(f"Rated Capacity: {rated_capacity:.2f} standard hours/week")

    # Calculate measured capacity
    measured_strategy: CapacityStrategy = MeasuredCapacityStrategy()
    calculator.set_strategy(measured_strategy)
    historical_data: List[int] = [200, 210, 215, 220]
    measured_capacity: float = calculator.calculate(historical_data)
    print(f"Measured Capacity: {measured_capacity:.2f} standard hours/week")
