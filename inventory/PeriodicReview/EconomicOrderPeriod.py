from math import sqrt
from abc import ABC, abstractmethod
from numbers import Number
from scipy.stats import norm

class Demand(ABC):
    @abstractmethod
    def get_demand(self):
        raise NotImplementedError

class FlexDemand(Demand):
    def __init__(self, mean: Number, std: Number):
        self.mean = mean
        self.std = std

    def get_demand(self) -> Number:
        return self.mean

class FixedDemand(Demand):
    def __init__(self, value: Number):
        self.value = value

    def get_demand(self) -> Number:
        return self.value


class PeriodicReviewSystem:
    def __init__(self, demander: Demand):
        self._demander = demander
        self._zscore: float = 1

    def set_service_level(self, level) -> None:
        self._zscore = norm.ppf(level)
        return None
    
    def set_demander(self, demander: Demand) -> None:
        self._demander = demander
        return None
    
    @property
    def zscore(self) -> float:
        return self._zscore
    
    @property
    def demand(self) -> Number:
        return self._demander.get_demand()

    def get_economic_order_period(self, carry_cost: Number, setup_cost: Number) -> float:
        return sqrt(2 * setup_cost / (carry_cost * self.demand))
    
    def get_max_inventory(self, review_period: Number, lead_time: Number) -> Number:
        period: Number = review_period + lead_time
        return self._demander.mean * period + self.zscore * self._demander.std * sqrt(period)
