from math import sqrt, ceil

class EOQ:
    def __init__(self, demand: int, carry_cost: float, setup_cost: float, quantity: float=None):
        self.demand = demand
        self.carry_cost = carry_cost
        self.setup_cost = setup_cost
        self.quantity = quantity

    def get_total_stocking_cost(self, quantity: float) -> float:
        return self.carry_cost * quantity / 2 + self.setup_cost * self.demand / quantity

    @property
    def economic_order_quantity(self) -> float:
        return sqrt(2 * self.demand * self.setup_cost / self.carry_cost)
    
    @property
    def order_times(self) -> int:
        return ceil(self.demand / self.economic_order_quantity)
    
    def get_order_frequency(self, length: int) -> int:
        return ceil(length * self.economic_order_quantity / self.demand)

    

    
    
