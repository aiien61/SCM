"""
Daily usage: 200 plastic bags
Delievery time: 4 days
Required safety stock: 100 plastic bags
"""
from ReorderPoint.SafetyStock import ReorderPoint
from icecream import ic

if __name__ == '__main__':
    ROP = ReorderPoint()
    ROP.calculate_expected_demand_during_lead_time(demand=200, lead_time=4)
    ROP.safety_stock = 100
    reorder_point = ROP.get_reorder_point(require_safety_stock=True)
    ic(reorder_point)
