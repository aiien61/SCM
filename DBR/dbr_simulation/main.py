from data_loader import load_orders, load_routing, generate_schedule_input
from scheduler import schedule_fifo
from datetime import datetime
from icecream import ic

orders = load_orders("./sample_orders.csv")
routing = load_routing("./sample_routing.csv")
schedule_input = generate_schedule_input(orders, routing)


scheduled = schedule_fifo(schedule_input, start_time=datetime(2024, 6, 17))
ic(scheduled)