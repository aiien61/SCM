from abc import ABC, abstractmethod
from typing import List
import numpy as np

class WorkCenter:
    def __init__(self, machines: int, hours_per_day: int, days_per_week: int):
        self.machines = machines
        self.hours_per_day = hours_per_day
        self.days_per_week = days_per_week
        self.available_time = self.calculate_available_time()

    def calculate_available_time(self):
        return self.machines * self.hours_per_day * self.days_per_week
    
class CapacityStrategy(ABC):
    @abstractmethod
    def calculate_capacity(slef, available_time, utilization, efficiency):
        raise NotImplementedError

class RatedCapacityStrategy(CapacityStrategy):
    def calculate_capacity(self, available_time: int, utilization: float, efficiency: float) -> float:
        return available_time * utilization * efficiency

class MeasuredCapacityStrategy(CapacityStrategy):
    def calculate_capacity(self, historical_data: List[int]) -> float:
        return np.mean(historical_data)
    
class CapacityCalculator:
    def __init__(self, strategy: CapacityStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: CapacityStrategy):
        self.strategy = strategy

    def calculate(self, *args, **kwargs) -> float:
        return self.strategy.calculate_capacity(*args, **kwargs)

if __name__ == "__main__":
    # Define a work centre
    work_center = WorkCenter(machines=4, hours_per_day=8, days_per_week=5)

    # Calculate Rated Capacity
    rated_strategy: CapacityStrategy = RatedCapacityStrategy()
    calculator: CapacityCalculator = CapacityCalculator(strategy=rated_strategy)
    rated_capacity: float = calculator.calculate(available_time=work_center.available_time, utilization=0.85, efficiency=1.1)
    print(f"Rated Capacity: {rated_capacity:.2f} standard hours/week")

    # Calculate Measured Capacity
    measured_strategy: CapacityStrategy = MeasuredCapacityStrategy()
    calculator.set_strategy(measured_strategy)
    historical_data: List[int] = [115, 120, 120, 125]
    measured_capacity: float = calculator.calculate(historical_data)
    print(f"Measured Capacity: {measured_capacity:.2f} standard hours/week")
