"""某森林木材供應商儲有數以千計的木材，以供應鄰近的木材商，該公司的總經理想了解如果使用EOQ模式已取代目前的經驗公式，
每年可以節省多少成本。他指示庫存管理人員，來進行其中某一項物料的分析（物料＃392一種橡木材），看看使用EOQ可以有多大的效益產生。
D = 每年平均10,000材橡木
C = 每年每材$0.4
S = 每次下單$5.5
目前每次的訂購量Q = 400材。
"""
from icecream import ic
from OrderQuantity.EconomicOrderQuantity import EOQ

if __name__ == '__main__':
    demand: int = 10_000
    carry_cost: float = 0.4
    setup_cost: float = 5.5
    current_quantity: int = 400
    inventory = EOQ(demand, carry_cost, setup_cost)

    tsc_now: float = inventory.get_total_stocking_cost(quantity=current_quantity)
    ic('目前每年採購費用：', tsc_now)
    
    eoq: int = inventory.economic_order_quantity
    ic('EOQ:', eoq)
    
    tsc_eoq: float = inventory.get_total_stocking_cost(quantity=eoq)
    ic('使用EOQ得採購成本：', tsc_eoq)

    ic(f'每年可節省之採購成本：{tsc_now - tsc_eoq:.2f}')

