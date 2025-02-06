from abc import ABC, abstractmethod
from typing import List
from icecream import ic
from dataclasses import dataclass
import numpy as np

@dataclass
class CapacityData:
    """Capacity data class for machines"""
    machines: int
    hours_per_day: float
    days_per_week: float
    actual_runtime: float
    standard_output: float
    actual_output: float

# Strategy pattern for all measurements
class CapacityStrategy(ABC):
    @abstractmethod
    def calculate(self, data: CapacityData) -> float:
        raise NotImplementedError
    
class AvailableTimeStrategy(CapacityStrategy):
    def calculate(self, data: CapacityData) -> float:
        return data.machines * data.hours_per_day * data.days_per_week
    
class UtilizationStrategy(CapacityStrategy):
    def calculate(self, data: CapacityData) -> float:
        available_time: float = AvailableTimeStrategy().calculate(data)
        return data.actual_runtime / available_time
    
class EfficiencyStrategy(CapacityStrategy):
    def calculate(self, data: CapacityData) -> float:
        return data.standard_output / data.actual_runtime
    
class RatedCapacityStrategy(CapacityStrategy):
    def calculate(self, data: CapacityData) -> float:
        available_time: float = AvailableTimeStrategy().calculate(data)
        utilization = UtilizationStrategy().calculate(data)
        efficiency = EfficiencyStrategy().calculate(data)
        return available_time * utilization * efficiency


class WorkCenter:
    def __init__(self, name: str, capacity_data: CapacityData):
        self.name = name
        self.capacity_data = capacity_data
        self.history: List[float] = []

    def calculate_capacity(self, strategy: CapacityStrategy) -> float:
        return strategy.calculate(self.capacity_data)
    
    def record_output(self, output: float) -> None:
        self.history.append(output)

    def get_demonstrated_capacity(self) -> float:
        if not self.history:
            return 0
        return np.mean(self.history)
    
class Factory:
    def __init__(self):
        self.work_centers: List[WorkCenter] = []

    def add_work_center(self, work_center: WorkCenter):
        self.work_centers.append(work_center)

    def get_total_rated_capacity(self) -> float:
        strategy = RatedCapacityStrategy()
        return np.sum([wc.calculate_capacity(strategy) for wc in self.work_cetners])
        
def main():
    # work centre data of bakery
    bakery_data = CapacityData(
        machines=4,
        hours_per_day=8,
        days_per_week=5,
        actual_runtime=136,
        standard_output=160,
        actual_output=176
    )

    # work centre
    bakery = WorkCenter("Baking Area", bakery_data)

    # measurements
    available_time = bakery.calculate_capacity(AvailableTimeStrategy())
    utilization = bakery.calculate_capacity(UtilizationStrategy())
    efficiency = bakery.calculate_capacity(EfficiencyStrategy())
    rated_capacity = bakery.calculate_capacity(RatedCapacityStrategy())

    # output
    print(f"工作中心: {bakery.name}")
    print(f"可用時間: {available_time:.1f} 小時/週")
    print(f"使用率: {round(utilization * 100, 2)}%")
    print(f"效率: {round(efficiency * 100, 2)}%")
    print(f"評定產能: {rated_capacity:.1f} 標準小時")

    # records actual runtime and calculate demonstrated capacity
    bakery.record_output(115)
    bakery.record_output(120)
    bakery.record_output(120)
    bakery.record_output(125)
    demonstrated_capacity = bakery.get_demonstrated_capacity()
    print(f"實證產能: {demonstrated_capacity:.1f} 標準小時/週")

if __name__ == "__main__":
    main()
