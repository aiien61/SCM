"""Determine Safety Stock"""
from icecream import ic

class ReorderPoint:
    def __init__(self):
        self.safety_stock: int = 0
        self.lead_time: int = 0
        self.demand: int = 0
        self.demand_in_lead_time: int = 0
    
    def get_reorder_point(self, require_safety_stock: bool=False):
        if require_safety_stock:
            return self.demand_in_lead_time + self.safety_stock
        else:
            return self.demand_in_lead_time


    def calculate_expected_demand_during_lead_time(self, demand: int, lead_time: int) -> bool:
        self.demand = demand
        self.lead_time = lead_time
        self.demand_in_lead_time = self.demand * self.lead_time
        return True
