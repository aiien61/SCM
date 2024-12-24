"""Climlab玩具製造商儲存了大量的D型玩具車，近期打算以數量折扣方式販賣這些玩具車。他們進行折扣的方案如下所示，
正常無折扣下每台玩具車販售$6.00;當客戶一次購買數量介於1,000~1,999時，提供3%的折扣，商品價格降低為$5.82;
而當客戶一次購買數量為2,000以上時，提供5%的折扣，商品價格繼續降低為$5.70。此外，客戶每一次的訂購須花費$49.00，
D型玩具車每年需求為5,000台，單位存貨持有成本為商品單價之20%，試問訂購多少數量會有最低的成本？

折扣方案    訂購數量    折扣百分比（％）    折扣價格（Ｐ）
   1       0~999        無折扣            $6.00   
   2     1,000~1,999      3              $5.82
   3       2,000~         5              $5.70
"""

from OrderQuantity.QuantityDiscountModel import QDM, DiscountModelManager
from icecream import ic
from typing import List
from itertools import pairwise
from math import inf

ic.disable()

if __name__ == '__main__':
    D: int = 5_000
    S: float = 49.00
    I: float = 0.2

    program_prices: List[float] = [6.0, 5.82, 5.70]
    program_quantity_boundareis: List[int] = [0, 1000, 2000, inf]

    discount_models: List[QDM] = []
    for P, boundary in zip(program_prices, pairwise(program_quantity_boundareis)):
        ic(P, boundary)
        model = QDM(D, S, I, P)
        model.min_Q = boundary[0]
        model.max_Q = boundary[1]
        discount_models.append(model)
        
    models_manager = DiscountModelManager(*discount_models)

    for model in models_manager.models:
        quantity = model.discount_model_quantity
        print(f'折扣方案1 -- 訂購數量: {quantity}\t年總成本: {model.get_total_stocking_cost(quantity)}')

    print(f'最低成本: {models_manager.get_min_cost()}\t訂購量: {models_manager.get_min_cost_quantity()}')


    # P1 = 6.0
    # qdm1 = QDM(D, S, I, P1)
    # qdm1.max_Q = 1000
    # Q1 = qdm1.discount_model_quantity
    # ic('折扣方案1 訂購數量:', Q1)

    # P2 = 5.82
    # qdm2 = QDM(D, S, I, P2)
    # qdm2.min_Q = 1_000
    # qdm2.max_Q = 1_999
    # Q2 = qdm2.discount_model_quantity
    # ic('折扣方案2 訂購數量:', Q2)

    # P3 = 5.70
    # qdm2 = QDM(D, S, I, P2)
    # qdm2.min_Q = 2000
    # Q3 = qdm2.discount_model_quantity
    # ic('折扣方案3 訂購數量:', Q3)

    # TSC_Q1 = QDM(D, S, I, P1).get_total_stocking_cost(quantity=Q1)
    # ic('折扣方案1 年總成本:', TSC_Q1)

    # TSC_Q2 = QDM(D, S, I, P2).get_total_stocking_cost(quantity=Q2)
    # ic('折扣方案2 年總成本:', TSC_Q2)

    # TSC_Q3 = QDM(D, S, I, P3).get_total_stocking_cost(quantity=Q3)
    # ic('折扣方案3 年總成本:', TSC_Q3)

