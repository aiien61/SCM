from scipy.stats import norm
from dataclasses import dataclass
from typing import List, Any
import numpy as np


class Demand:
    def __init__(self, records: List[int] = None):
        self.records = [] if records is None else records
        self.fixed_value: Any = None
        self._is_fixed: bool = False
        self._mean: float = None
        self._std: float = None
        if self.records:
            self._mean = np.mean(records)
            self._std = np.std(records)

    def set_fixed_value(self, value: int) -> None:
        self.fixed_value = value
        self._is_fixed = True
        return None
    
    @property
    def is_fixed(self) -> bool:
        return self._is_fixed
        
    @property
    def mean(self):
        return self._mean

    @mean.setter
    def mean(self, new_mean: float):
        self._mean = new_mean
        return None
    
    @property
    def std(self):
        return self._std
    
    @std.setter
    def std(self, new_std: float):
        self._std = new_std
        return None


class LeadTime:
    def __init__(self):
        self.fixed_value: Any = None
        self._is_fixed: bool = False
        self._mean: float = None
        self._std: float = None

    def set_fixed_value(self, value: Any) -> None:
        self.fixed_value = value
        self._is_fixed = True
        return None
    
    @property
    def is_fixed(self) -> bool:
        return self._is_fixed

    @property
    def mean(self):
        return self._mean
    
    @mean.setter
    def mean(self, new_mean: float):
        self._mean = new_mean
        return None
    
    @property
    def std(self):
        return self._std
    
    @std.setter
    def std(self, new_std: float):
        self._std = new_std
        return None


class Inventory:
    def __init__(self) -> int:
        self._base: float = 0
        self._multiplier: int = 1

    @property
    def base(self):
        return self._base
    
    @base.setter
    def base(self, new_base: float):
        self._base = new_base
        return None
    
    @property
    def multiplier(self):
        return self._multiplier
    
    @multiplier.setter
    def multiplier(self, new_multiplier: float):
        self._multiplier = new_multiplier
        return None


class ReorderPoint:
    def __init__(self, demand: Demand, lead_time: LeadTime, inventory: Inventory):
        self.demand = demand
        self.lead_time = lead_time
        self.inventory = inventory

    @property
    def z_score(self):
        return self.inventory.multiplier
    
    @property
    def safety_stock(self):
        if self.lead_time.is_fixed and self.demand.is_fixed:
            # fixed demand and fixed lead time
            self.inventory.base = 0

        elif self.lead_time.is_fixed and not self.demand.is_fixed:
            # fixed lead time
            self.inventory.base = np.sqrt(self.lead_time.fixed_value) * self.demand.std
        
        elif self.demand.is_fixed and not self.lead_time.is_fixed:
            # fixed demand
            self.inventory.base = self.demand.fixed_value * self.lead_time.std

        else:
            # demand and lead time are not fixed
            self.inventory.base = np.sqrt(self.lead_time.mean * np.pow(self.demand.std, 2) + np.pow(self.demand.mean * self.lead_time.std, 2))

        return self.inventory.multiplier * self.inventory.base

    def set_service_level(self, level: float) -> None:
        self.inventory.multiplier = norm.ppf(level)

    def get_service_level(self, reorder_point: int) -> float:
        if self.lead_time.is_fixed:
            zscore = (reorder_point - self.demand.mean * self.lead_time.fixed_value) / self.inventory.base
            return norm.cdf(zscore)

    def get_reorder_point(self) -> int:
        final_lead_time: int = self.lead_time.mean
        final_demand: int = self.demand.mean

        if self.lead_time.is_fixed:
            final_lead_time = self.lead_time.fixed_value
        
        if self.demand.is_fixed:
            final_demand = self.demand.fixed_value
            
        expected_demand_during_lead_time: float = final_demand * final_lead_time
        return expected_demand_during_lead_time + self.safety_stock
