"""某產品單價為$20，每年需訂購16,000個，每次的訂購成本為$60，而每年單位存貨的持有成本$3，試問其經濟訂購期間EOP為何？
（假設每年有250個工作天）
"""

from OrderQuantity.EconomicOrderQuantity import EOQ

DEMAND: int = 16_000
CARRY_COST: int = 3
SETUP_COST: int = 60
PRICE: int = 20
WORKDAYS_IN_YEAR: int = 250

eoq = EOQ(DEMAND, CARRY_COST, SETUP_COST)
eop_by_year: float = eoq.economic_order_quantity / DEMAND
eop_by_day: float = eop_by_year * WORKDAYS_IN_YEAR
print(eop_by_day)
