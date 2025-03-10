"""模擬運輸路線的簡單最佳化
"""
import math
from typing import List, Tuple
from rich import print


def optimize_delivery_route(locations: List[Tuple[float, float]], start: Tuple[float, float]) -> List[Tuple[float, float]]:
    """
    最佳化運輸路線（從起點開始，選擇最近的點）
    :param locations: 配送點坐標列表
    :param start: 起點坐標
    :return: 優化後的路線
    """
    route = [start]
    unvisited = locations.copy()

    while unvisited:
        current = route[-1]
        next_location = min(unvisited, key=lambda loc: math.dist(current, loc))
        route.append(next_location)
        unvisited.remove(next_location)
    
    return route

def main():
    # 運輸最佳化：模擬配送路線
    start_point = (0, 0)  # 起點
    delivery_points = [(2, 3), (5, 1), (1, 4), (3, 2)]  # 配送點
    optimized_route = optimize_delivery_route(delivery_points, start_point)
    print("\n最佳化配送路線：")
    for point in optimized_route:
        print(f"-> {point}")

if __name__ == "__main__":
    main()