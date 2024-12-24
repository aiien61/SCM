"""假設管理階層決定只能容許某品項一年一次缺料。此品項年需求量為52,000個，訂購量為2,600個，採購前置時間為一週，
且在前置時間一週內需求的標準差為100個。試計算：
1. 每年的訂購次數
2. 服務水準
3. 安全庫存
4. 在訂購點
"""
from math import ceil
from icecream import ic
from ReorderPoint.VariabilityOfDemandAndLeadTime import Demand, LeadTime, Inventory, ReorderPoint

DEMAND_YEARLY: int = 52_000
ORDER_YEARLY: int = 2_600
DEMAND_STD: int = 100
DEMAND_MEAN: float = DEMAND_YEARLY / 52
LEAD_TIME: int = 1

if __name__ == '__main__':
    times_to_order: int = ceil(DEMAND_YEARLY / ORDER_YEARLY)
    ic(times_to_order)

    service_level: float = (times_to_order - 1) / times_to_order
    ic(service_level)

    demand: Demand = Demand()
    lead_time: LeadTime = LeadTime()
    inventory: Inventory = Inventory()

    demand.mean = DEMAND_MEAN
    demand.std = DEMAND_STD
    lead_time.set_fixed_value(value=LEAD_TIME)
    inventory.base = DEMAND_STD

    ROP = ReorderPoint(demand=demand, lead_time=lead_time, inventory=inventory)
    ROP.set_service_level(level=service_level)
    safety_stock: float = round(ROP.safety_stock, 1)
    ic(safety_stock)

    reorder_point: int = round(ROP.get_reorder_point(), 1)
    ic(reorder_point)
