"""
Daily required milk: 3 bottles
Delivery time: 2 days
"""
from ReorderPoint.SafetyStock import ReorderPoint
from icecream import ic

if __name__ == '__main__':
    demand: int = 3
    lead_time: int = 2

    ROP = ReorderPoint()
    ROP.calculate_expected_demand_during_lead_time(demand, lead_time)
    reorder_point = ROP.get_reorder_point(require_safety_stock=False)
    ic(reorder_point)
