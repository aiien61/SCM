"""某藥局藥劑師平均每天使用量為50毫克，根據以往紀錄每天需求量呈常態分佈，每日需求量標準差為5毫克，前置時間固定為4天，
該藥劑師希望缺貨的機率不要超過1%，試問：
1. 需準備多少安全庫存？
2. 決定在訂購點應為幾毫克？
3. 如果在訂購點訂於215毫克，則其服務水準為多少？
"""
from ReorderPoint.VariabilityOfDemandAndLeadTime import Demand, LeadTime, Inventory, ReorderPoint
from icecream import ic

DEMAND_MEAN: int = 50
DEMAND_STD: int = 5
LEAD_TIME: int = 4
SERVICE_LEVEL: float = 0.99

if __name__ == '__main__':
    demand: Demand = Demand()
    lead_time: LeadTime = LeadTime()
    inventory: Inventory = Inventory()
    
    demand.mean = DEMAND_MEAN
    demand.std = DEMAND_STD
    lead_time.set_fixed_value(LEAD_TIME)

    ROP = ReorderPoint(demand, lead_time, inventory)
    ROP.set_service_level(level=0.99)
    safety_stock: float = round(ROP.safety_stock, 1)
    ic(safety_stock)

    reorder_point: float = round(ROP.get_reorder_point(), 1)
    ic(reorder_point)

    service_level: float = round(ROP.get_service_level(reorder_point=215), 4)
    ic(service_level)


    