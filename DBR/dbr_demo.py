import polars as pl
import plotly.express as px
from typing import List, Dict
from enum import Enum, auto
from rich import print

class Workcenter(Enum):
    W1 = auto()
    W2 = auto()
    W3 = auto()


# orders data
orders: List[dict] = [
    # order id, required time at workcentre 1, required time at workcentre 2, required time at workcentre 3
    {"order_id": "A", Workcenter.W1: 2, Workcenter.W2: 5, Workcenter.W3: 2},
    {"order_id": "B", Workcenter.W1: 1, Workcenter.W2: 3, Workcenter.W3: 2},
    {"order_id": "C", Workcenter.W1: 2, Workcenter.W2: 6, Workcenter.W3: 1}
]

# set bottleneck
bottleneck: Workcenter = Workcenter.W2
buffer_time: int = 2  # buffer time

# available time of each workcentre (all initiate at time 0)
available_time: Dict[Workcenter, int] = {
    Workcenter.W1: 0, 
    Workcenter.W2: buffer_time, 
    Workcenter.W3: 0
}

# collect scheduling data
schedule_data: List[dict] = []

# dispatch resources based on the bottleneck W2 (Drum)
for order in orders:
    order_id: str = order["order_id"]

    # W2 is the bottleneck
    start_w2: int = available_time[Workcenter.W2]
    end_w2: int = start_w2 + order[Workcenter.W2]

    # Rope: 
    end_w1: int = start_w2 - buffer_time
    start_w1: int = max(available_time[Workcenter.W1], end_w1 - order[Workcenter.W1])
    end_w1 = start_w1 + order[Workcenter.W1]

    # 
    start_w3: int = max(available_time[Workcenter.W3], end_w2)
    end_w3: int = start_w3 + order[Workcenter.W3]

    # update 
    available_time[Workcenter.W1] = end_w1
    available_time[Workcenter.W2] = end_w2
    available_time[Workcenter.W3] = end_w3

    # 
    schedule_data += [
        {"Task": f"{order_id}_W1", "Start": start_w1, "Finish": end_w1, "Station": Workcenter.W1.name},
        {"Task": f"{order_id}_W2", "Start": start_w2, "Finish": end_w2, "Station": Workcenter.W2.name},
        {"Task": f"{order_id}_W3", "Start": start_w3, "Finish": end_w3, "Station": Workcenter.W3.name}
    ]

# create dataframe
df: pl.DataFrame = pl.DataFrame(schedule_data)

# convert to pd.DataFrame
df = df.to_pandas()

print(df)

# draw Gantt chart using plotly
fig = px.timeline(df, x_start="Start", x_end="Finish", y="Station", color="Task", title="DBR 排程圖")
fig.update_yaxes(autorange="reversed")

# Tell Plotly to treat the x-axis as numbers, not dates.
fig.update_xaxes(type="linear")
fig.show()
