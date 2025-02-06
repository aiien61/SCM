from abc import ABC, abstractmethod
from typing import List, Dict
from icecream import ic
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum, auto
import numpy as np

class ResourceType(Enum):
    MACHINE = auto()
    WORKER = auto()
    TOOLING = auto()

@dataclass
class ResourceData:
    quantity: int
    hours_per_day: int
    days_per_week: int
    actual_runtime: float
    standard_output: float
    actual_output: float
    efficiency_factor: float

@dataclass
class CapacityData:
    hours_per_day: int
    days_per_week: int
    actual_runtime: float
    standard_output: float
    actual_output: float
    efficiency_factor: float


class ResourceComponent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def calculate_available_time(self) -> float: raise NotImplementedError

    @abstractmethod
    def calculate_utilization(self) -> float: raise NotImplementedError

    @abstractmethod
    def calculate_efficiency(self) -> float: raise NotImplementedError

    @abstractmethod
    def calculate_rated_capacity(self) -> float: raise NotImplementedError

class Resource(ResourceComponent):
    def __init__(self, name: str, type_: ResourceType, data: CapacityData):
        super().__init__(name)
        self.type_ = type_
        self.data = data
    
    