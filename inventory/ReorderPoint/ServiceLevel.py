from scipy.stats import norm
from math import ceil
from icecream import ic


class ServiceLevel:
    def __init__(self, demand_mean: float, demand_std: float, lead_time: int):
        self.mean: float = demand_mean
        self.std: float = demand_std
        self.lead_time: int = lead_time
        self._zscore: float = 1

    def set_service_level(self, level: float) -> float:
        self._zscore = norm.ppf(level)
        

    def get_safety_stock(self, std_multiplier: float=None) -> int:
        if not std_multiplier:
            std_multiplier = self._zscore
        return ceil(std_multiplier * self.std)

    def get_reorder_point(self, std_multiplier: float=None) -> int:
        expected_demand_during_lead_time: float = self.mean * self.lead_time
        safety_stock: int = self.get_safety_stock(std_multiplier)
        return ceil(expected_demand_during_lead_time + safety_stock)
