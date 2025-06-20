from typing import Set
from data_loader import load_orders, load_routing, generate_schedule_input
from scheduler import create_ruins_schedule
from ruin_leveler import level_the_ruins
from datetime import timedelta
from icecream import ic
from rich import print

# 載入資料
orders = load_orders("./sample_orders.csv")
routing = load_routing("./sample_routing.csv")
schedule_input = generate_schedule_input(orders, routing)

# DBR 參數
SHIPPING_BUFFER: timedelta = timedelta(days=2)
BOTTLENECKS: Set[str] = {"Sew1"}

# --- 1. 建立廢墟 (Create Ruins) ---
print("[bold green]1. 建立廢墟 (倒推排程結果):[/bold green]")
ruins_schedule = create_ruins_schedule(schedule_input, SHIPPING_BUFFER)
ic(ruins_schedule)
# print("[yellow]觀察：Sew1 (瓶頸) 在 2024-06-25 04:00:00 左右有時間衝突！[/yellow]")

print("-" * 80)

# --- 2. 剷平廢墟 (Level the Ruins) ---
print("[bold green]2. 剷平廢墟後 (最終排程):[/bold green]")
leveled_schedule = level_the_ruins(ruins_schedule, BOTTLENECKS)
ic(ruins_schedule)
print(leveled_schedule)
# print("[yellow]觀察：Sew1 上的工作已依序排開，A001 的前序工作 (Cutting) 也被同步推遲。[/yellow]")
