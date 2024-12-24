"""
Demands in the past ten weeks:
week1   1,200
week2   1,000
week3     800
week4     900
week5   1,400
week6   1,100
week7   1,100
week8     700
week9   1,000
week10    800

Total: 10,000
Lead time: 1 week

1. calculate the mean and standard deviation of demands
2. if safety stock = 2 * standard deviation, calculate safety stock & reorder point
3. if service level = 95%, calculate safety stock & reorder point
"""
from ReorderPoint.ServiceLevel import ServiceLevel
from icecream import ic
from typing import List
import numpy as np

if __name__ == '__main__':
    lead_time: int = 1
    demands: List[int] = np.array([1_200, 1_000, 800, 900, 1_400, 1_100, 1_100, 700, 1_000, 800])
    mean_demand: float = np.mean(demands)
    std_demand: float = np.std(demands)
    ic(mean_demand, std_demand)

    ROP = ServiceLevel(mean_demand, std_demand, lead_time)
    safety_stock: int = ROP.get_safety_stock(std_multiplier=2)
    reorder_point: int = ROP.get_reorder_point(std_multiplier=2)
    ic(safety_stock, reorder_point)

    service_level: float = 0.95
    ROP.set_service_level(level=service_level)
    safety_stock = ROP.get_safety_stock()
    reorder_point = ROP.get_reorder_point()
    ic(safety_stock, reorder_point)
