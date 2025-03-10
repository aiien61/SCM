"""使用EOQ模型達到庫存訂貨量最佳化
"""
import math
from rich import print

# 經濟訂貨量（EOQ）計算
def calculate_eoq(demand: float, ordering_cost: float, holding_cost: float) -> float:
    """
    計算經濟訂貨量
    :param demand: 年需求量
    :param ordering_cost: 每次訂貨成本
    :param holding_cost: 單位持有成本（每年）
    :return: 最佳訂貨量
    """
    return math.sqrt((2 * demand * ordering_cost) / holding_cost)

if __name__ == "__main__":
    # 庫存最佳化：計算EOQ
    annual_demand: int = 12_000  # 年需求量（單位：件）
    ordering_cost: int = 50      # 每次訂貨成本（單位：元）
    holding_cost: int = 2        # 單位持有成本（元/件/年）
    eoq: float = calculate_eoq(annual_demand, ordering_cost, holding_cost)
    print(f"最佳訂貨量 (EOQ): {eoq:.2f} 件")
    print(f"訂貨次數/年: {annual_demand / eoq:.2f} 次")
