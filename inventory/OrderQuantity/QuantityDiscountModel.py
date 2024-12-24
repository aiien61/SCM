from math import sqrt, inf
from typing import List
from icecream import ic

class QDM:
    """
    D: demand
    S: setup cost
    Q: quantity
    I: portion of carry cost on price
    P: price
    """

    def __init__(self, D: int, S: float, I: float, P: float, Q=None):
        self.D = D
        self.S = S
        self.Q = Q
        self.I = I
        self.P = P
        self.Q = Q
        self._min_Q = 0
        self._max_Q = inf

    @property
    def min_Q(self) -> int:
        return self._min_Q
    
    @min_Q.setter
    def min_Q(self, new_min_Q: int) -> None:
        self._min_Q = new_min_Q
        return None
    
    @property
    def max_Q(self) -> int:
        return self._max_Q
    
    @max_Q.setter
    def max_Q(self, new_max_Q: int) -> None:
        self._max_Q = new_max_Q
        return None
    
    @property
    def discount_model_quantity(self):
        ic.disable()
        
        dmq: float = sqrt(2 * self.D * self.S / (self.I * self.P))
        ic(dmq)
        ic(self._min_Q)
        ic(self._max_Q)
        if dmq < self._min_Q:
            return self._min_Q
        elif self._max_Q < dmq:
            return self._max_Q
        else:
            return round(dmq)
        
    def get_total_stocking_cost(self, quantity: int) -> float:
        return (quantity / 2) * self.I * self.P + (self.D / quantity) * self.S + self.P * self.D


class DiscountModelManager:
    def __init__(self, *discount_models: List[object]):
        self.models = discount_models

    def get_min_cost(self) -> float:
        return min([model.get_total_stocking_cost(model.discount_model_quantity) for model in self.models])
    
    def get_min_cost_quantity(self):
        sorted_models = sorted(self.models, key=lambda model: model.discount_model_quantity)
        min_model = sorted_models[0]
        return min_model.discount_model_quantity
