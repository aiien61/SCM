import pandas as pd
import altair as alt
from typing import List, Dict
from enum import Enum, auto

# Explicitly tell Altair to use the 'browser' renderer
alt.renderers.enable('browser')


class Workcenter(Enum):
    W1 = auto()
    W2 = auto()
    W3 = auto()


orders: List[dict] = [
    {"order_id": "A", Workcenter.W1: 2, Workcenter.W2: 5, Workcenter.W3: 2},
    {"order_id": "B", Workcenter.W1: 1, Workcenter.W2: 3, Workcenter.W3: 2},
    {"order_id": "C", Workcenter.W1: 2, Workcenter.W2: 6, Workcenter.W3: 1}
]

bottleneck: Workcenter = Workcenter.W2
buffer_time: int = 2

available_time: Dict[Workcenter, int] = {
    Workcenter.W1: 0,
    Workcenter.W2: buffer_time,
    Workcenter.W3: 0
}

schedule_data: List[dict] = []

for order in orders:
    order_id: str = order["order_id"]
    start_w2: int = available_time[Workcenter.W2]
    end_w2: int = start_w2 + order[Workcenter.W2]
    end_w1_required: int = start_w2 - buffer_time
    start_w1: int = max(available_time[Workcenter.W1], end_w1_required - order[Workcenter.W1])
    end_w1 = start_w1 + order[Workcenter.W1]
    start_w3: int = max(available_time[Workcenter.W3], end_w2)
    end_w3: int = start_w3 + order[Workcenter.W3]
    available_time[Workcenter.W1] = end_w1
    available_time[Workcenter.W2] = end_w2
    available_time[Workcenter.W3] = end_w3
    schedule_data += [
        {"Task": f"{order_id}_W1", "Start": start_w1,
            "Finish": end_w1, "Station": Workcenter.W1.name},
        {"Task": f"{order_id}_W2", "Start": start_w2,
            "Finish": end_w2, "Station": Workcenter.W2.name},
        {"Task": f"{order_id}_W3", "Start": start_w3,
            "Finish": end_w3, "Station": Workcenter.W3.name}
    ]

# Create the Pandas DataFrame
df = pd.DataFrame(schedule_data)
print("--- DataFrame successfully created ---")
print(df)
print("------------------------------------")


# --- Part 2: NEW Interactive plotting section using Altair ---

chart = alt.Chart(df).mark_bar(
    size=25
).encode(
    # Set the y-axis to be the 'Station', treating it as a categorical variable.
    # We provide a sort order to ensure W1 is at the top.
    y=alt.Y('Station:N', 
            sort=['W1', 'W2', 'W3'], 
            title='Station', 
            axis=alt.Axis(
                titleAngle=0,       # Set title angle to 0 for horizontal
                titleAlign='right',  # Align the title text
                titleY=-15,         # Move title up (negative is up)
                titleX=35,          # Move title right to give it space
                labelFontSize=12,   # Also slightly increase axis label font size
                titleFontSize=14    # Increase axis title font size
            )),

    # Set the x-axis start and end points. Altair has special x and x2 encodings for this.
    x=alt.X('Start:Q', title='Time'),
    x2=alt.X2('Finish:Q'),

    # Color the bars by the 'Task' column.
    color=alt.Color('Task:N', 
                    title='Task', 
                    legend=alt.Legend(
                        titleFontSize=14,
                        labelFontSize=12,
                        symbolSize=150  # Makes the colored squares in the legend bigger
                    )),

    # Create an interactive tooltip that shows details on hover.
    tooltip=[
        alt.Tooltip('Task:N'),
        alt.Tooltip('Start:Q'),
        alt.Tooltip('Finish:Q')
    ]
).properties(
    title='DBR 排程圖 (Interactive)',
    width=1200,  # Increased from 800
    height=400   # Added a height property to make the chart taller
)

# To be safe, let's save to an HTML file first, just like we did with Plotly.
# This is the most reliable way to view the chart.
chart.save('dbr_chart_altair.html')

print("\nInteractive chart has been saved to dbr_chart_altair.html. Please open this file in your browser.")

# You can also try showing it directly, which may work now.
chart.show()
