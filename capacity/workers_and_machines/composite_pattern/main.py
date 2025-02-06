from abc import ABC, abstractmethod
from typing import List, Dict
from icecream import ic
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum, auto
import numpy as np

# Resource Types
class ResourceType(Enum):
    MACHINE = auto()
    WORKER = auto()
    WORKSTATION = auto()

# Resource Data Class
@dataclass
class ResourceData:
    quantity: int
    hours_per_day: float
    days_per_week: int
    actual_runtime: float
    standard_output: float
    actual_output: float
    efficiency_factor: float  # e.g. skill level, machinery efficiency

class ResourceComponent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def calculate_available_time(self) -> float:
        raise NotImplementedError
    
    @abstractmethod
    def calculate_utilization(self) -> float:
        raise NotImplementedError
    
    @abstractmethod
    def calculate_efficiency(self) -> float:
        raise NotImplementedError
    
    @abstractmethod
    def calculate_rated_capacity(self) -> float:
        raise NotImplementedError

# Resource Class
class Resource(ResourceComponent):
    def __init__(self, name: str, resource_type: ResourceType, data: ResourceData):
        super().__init__(name)
        self.resource_type = resource_type
        self.data = data
        self.history: List[float] = []

    def calculate_available_time(self) -> float:
        return self.data.quantity * self.data.hours_per_day * self.data.days_per_week
    
    def calculate_utilization(self) -> float:
        available_time = self.calculate_available_time()
        return (self.data.actual_runtime / available_time) if available_time > 0 else 0
    
    def calculate_efficiency(self) -> float:
        return (self.data.actual_output / self.data.standard_output) * self.data.efficiency_factor
    
    def calculate_rated_capacity(self) -> float:
        available_time = self.calculate_available_time()
        utilization = self.calculate_utilization()
        efficiency = self.calculate_efficiency()
        return available_time * utilization * efficiency
    
    def record_output(self, output: float) -> bool:
        self.history.append(output)
        return True
    
    def get_demonstrated_capacity(self) -> float:
        return np.mean(self.history) if self.history else 0
    
# Work Centre Class
class WorkCenter(ResourceComponent):
    def __init__(self, name: str):
        super().__init__(name)
        self.resources: List[ResourceComponent] = []
    
    def add_resource(self, resource: ResourceComponent):
        self.resources.append(resource)
    
    def remove_resource(self, resource: ResourceComponent):
        self.resources.remove(resource)
    
    def calculate_available_time(self) -> float:
        return np.sum([r.calculate_available_time() for r in self.resources])
    
    def calculate_utilization(self) -> float:
        total_actual: float = np.sum([r.calculate_available_time() * r.calculate_utilization() for r in self.resources])
        total_available: float = self.calculate_available_time()
        return (total_actual / total_available) if total_available > 0 else 0
    
    def calculate_efficiency(self) -> float:
        return np.mean([r.calculate_efficiency() for r in self.resources]) if self.resources else 0
    
    def calculate_rated_capacity(self) -> float:
        return np.sum([r.calculate_rated_capacity() for r in self.resources])

# Resource factory
class ResourceFactory:
    @staticmethod
    def create_resoruce(name: str, resource_type: ResourceType, data: ResourceData):
        return Resource(name, resource_type, data)

# Capacity report generator:
class CapacityReportGenerator:
    @staticmethod
    def generate_report(component: ResourceComponent) -> Dict:
        return {
            'name': component.name,
            'available_time': component.calculate_available_time(),
            'utilization': component.calculate_utilization(),
            'efficiency': component.calculate_efficiency(),
            'rated_capacity': component.calculate_rated_capacity()
        }
    
# demo
def main():
    # resource data
    machine_data: ResourceData = ResourceData(
        quantity=2,
        hours_per_day=8,
        days_per_week=5,
        actual_runtime=70,
        standard_output=80,
        actual_output=85,
        efficiency_factor=1.0
    )

    worker_data: ResourceData = ResourceData(
        quantity=3,
        hours_per_day=8,
        days_per_week=5,
        actual_runtime=110,
        standard_output=100,
        actual_output=105,
        efficiency_factor=0.9  # considering staff's skill level
    )

    # factory
    factory: ResourceFactory = ResourceFactory()

    # initialise resources
    machines: Resource = factory.create_resoruce("oven", ResourceType.MACHINE, machine_data)
    workers: Resource = factory.create_resoruce("baker", ResourceType.WORKER, worker_data)

    # initialise work centre
    bakery: WorkCenter = WorkCenter("baking area")
    bakery.add_resource(machines)
    bakery.add_resource(workers)

    # generate report
    report = CapacityReportGenerator.generate_report(bakery)

    # overall report
    ic(report)

    # categorical report
    for resource in [machines, workers]:
        resource_report: dict = CapacityReportGenerator.generate_report(resource)
        ic(resource_report)

if __name__ == '__main__':
    main()
