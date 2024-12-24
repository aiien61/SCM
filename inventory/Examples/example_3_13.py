"""零售店的香菸是採固定訂購期間系統，香菸的需求率會變動，且呈常態分佈，有關資料如下：
Demand mean: 30包 / 天
Demand std: 3包 / 天
假設庫存量在訂購時為71包，LT=2天，每隔一週（7天）下訂單補貨，試求服務水在99%的最高庫存量為何？訂購的數量為何？
"""
from PeriodicReview.EconomicOrderPeriod import PeriodicReviewSystem, FlexDemand
from icecream import ic
from math import ceil

DEMAND_MEAN: int = 30
DEMAND_STD: int = 3
LEAD_TIME: int = 2
REVIEW_PERIOD: int = 7
SERVICE_LEVEL: float = 0.99
STOCK: int = 71

if __name__ == '__main__':
    demander: FlexDemand = FlexDemand(mean=DEMAND_MEAN, std=DEMAND_STD)
    prs = PeriodicReviewSystem(demander)
    prs.set_service_level(0.99)
    inventory_max: int = ceil(prs.get_max_inventory(review_period=REVIEW_PERIOD, lead_time=LEAD_TIME))
    ic(inventory_max)

    required_quantity: int = inventory_max - STOCK
    ic(required_quantity)
