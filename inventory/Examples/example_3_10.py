"""工廠的自動燃燒機每天使用2.1加侖的石油，石油購買的前置時間呈常態分佈，平均為6天，標準差為2天，工廠的服務水準政策為98%，
試求應準備多少的安全庫存，而再訂購點如何決定？
"""
from ReorderPoint.VariabilityOfDemandAndLeadTime import Demand, LeadTime, Inventory, ReorderPoint
from icecream import ic

DEMAND_FIXED: float = 2.1
LEAD_TIME_MEAN: int = 6
LEAD_TIME_STD: int = 2
SERVICE_LEVEL: float = 0.98

if __name__ == '__main__':
    demand: Demand = Demand()
    lead_time: LeadTime = LeadTime()
    inventory: Inventory = Inventory()

    demand.set_fixed_value(DEMAND_FIXED)
    lead_time.mean = 6
    lead_time.std = 2

    ROP = ReorderPoint(demand, lead_time, inventory)
    ROP.set_service_level(0.98)
    safety_stock: float = round(ROP.safety_stock, 3)
    ic(safety_stock)

    reorder_point: float = round(ROP.get_reorder_point(), 2)
    ic(reorder_point)

