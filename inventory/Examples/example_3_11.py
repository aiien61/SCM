"""餐廳販賣啤酒，已知每天消費需求量為常態分佈，平均為每天150罐，標準差每天為10罐；交貨前置時間亦呈常態分配，平均為6天，
標準差為1天，試求該餐廳欲維持在90%的服務水準下之再訂購點
"""
from ReorderPoint.VariabilityOfDemandAndLeadTime import Demand, LeadTime, Inventory, ReorderPoint
from icecream import ic

DEMAND_MEAN: int = 150
DEMAND_STD: int = 10
LEAD_TIME_MEAN: int = 6
LEAD_TIME_STD: int = 1
SERVICE_LEVEL: float = 0.9

if __name__ == '__main__':
    demand: Demand = Demand()
    lead_time: LeadTime = LeadTime()
    inventory: Inventory = Inventory()

    demand.mean = DEMAND_MEAN
    demand.std = DEMAND_STD
    lead_time.mean = LEAD_TIME_MEAN
    lead_time.std = LEAD_TIME_STD

    ROP = ReorderPoint(demand, lead_time, inventory)
    ROP.set_service_level(level=SERVICE_LEVEL)
    reorder_point: float = round(ROP.get_reorder_point())
    ic(reorder_point)