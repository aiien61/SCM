"""某水電公司有鄰近生產工廠可以生產#856水閥，這種水閥在工廠生產完畢後會送至水電公司倉庫儲存以備隔一段時間後使用。
水閥之儲存費用、訂購或準備費用及每年的需求量，大約維持一定。因此，水閥是每天逐漸生產再送至倉庫儲存使用，
而不是一次生產大批量送至倉庫。公司主管想了解已逐漸生產再送至倉庫儲存使用與一次生產大批量送至倉庫兩者間的成本差異。

D=每年10,000個水閥
C=每年每個水閥$0.40
S=每次下單$5.50
d=每天40個水閥（每年10,000個水閥，每年250個工作天）
p=每天120個水閥
"""

from OrderQuantity.EconomicManufacturingQuantity import EMQ
from OrderQuantity.EconomicOrderQuantity import EOQ
from icecream import ic

if __name__ == '__main__':

    p: int = 120
    d: int = 40
    D: int = 10_000
    C: float = .4
    S: float = 5.5

    inventory = EMQ(p, d, D, C, S)

    emq: float = inventory.economic_manufacturing_quantity
    ic('EMQ:', inventory.economic_manufacturing_quantity)

    tsc_emq = inventory.get_total_stocking_cost(emq)
    ic('TSC by EMQ:', inventory.get_total_stocking_cost(emq))

    inventory = EOQ(demand=D, carry_cost=C, setup_cost=S)
    eoq: float = inventory.economic_order_quantity
    ic('EOQ:', inventory.economic_order_quantity)

    tsc_eoq = inventory.get_total_stocking_cost(quantity=eoq)
    ic('TSC by EOQ:', inventory.get_total_stocking_cost(quantity=eoq))

    ic('TSC by EOQ - TSC by EMQ =', tsc_eoq - tsc_emq)


