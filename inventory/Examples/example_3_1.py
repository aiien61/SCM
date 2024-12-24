"""某國際輪胎公司之國內配銷商期望每年銷售某類輪胎9,600條。每條輪胎的年存貨持有成本為$16，訂購成本為$75，配銷商每年營業228天
"""
from icecream import ic
from OrderQuantity.EconomicOrderQuantity import EOQ

if __name__ == '__main__':
    demand: int = 9_600
    carry_cost: int = 16
    setup_cost: int = 75

    inventory = EOQ(demand, carry_cost, setup_cost)

    ic(inventory.economic_order_quantity)
    ic('每年訂購次數：', inventory.order_times)
    ic('訂購週期的長度：', inventory.get_order_frequency(length=288))
