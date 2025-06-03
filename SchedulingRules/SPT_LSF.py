from collections import deque, defaultdict
from icecream import ic
from dataclasses import dataclass
from enum import Enum
from rich.console import Console
import matplotlib.pyplot as plt

console = Console()

# Job data: list of tasks per job in the form (machine, duration)
jobs = {
    1: [('A', 3), ('B', 3), ('C', 2)],
    2: [('A', 5), ('C', 2)],
    3: [('B', 4), ('A', 4), ('C', 3)],
    4: [('B', 3), ('C', 5), ('A', 2)],
    5: [('C', 5), ('B', 4)],
    6: [('C', 2), ('A', 5), ('B', 5)],
}

# Due dates
due_dates = {
    1: 10,
    2: 13,
    3: 12,
    4: 18,
    5: 14,
    6: 15,
}

# Simulate scheduling with SPT (投料) and LSF (派工)

class MachineType(Enum):
    A = "A"
    B = "B"
    C = "C"

class Machine:
    def __init__(self, type_: MachineType):
        self.type = type_
        self.timeline = []  # (start, end, job_id)
        self.available_at = 0

    def __str__(self):
        return f"{self.type.name}(timeline={self.timeline}, available_at={self.available_at})"
    
    def __repr__(self):
        return str(self)


# Re-simulate to extract detailed step-by-step 投料與派工紀錄
machines = {'A': Machine(type_=MachineType.A), 
            'B': Machine(type_=MachineType.B), 
            'C': Machine(type_=MachineType.C)}

job_queues = {j: deque(steps) for j, steps in jobs.items()}
job_progress = {j: 0 for j in jobs}
job_time_remaining = {j: sum(d for _, d in steps) for j, steps in jobs.items()}
job_ready_time = {j: 0 for j in jobs}

time = 0
in_progress = []
finished_jobs = set()
event_log = []

while len(finished_jobs) < len(jobs):
    ic(time)
    ic(finished_jobs)
    ic(job_queues)

    # Step 1: collect ready tasks (SPT投料)
    console.print("collect ready tasks", style="red")
    ready_tasks = []
    for job_id, queue in job_queues.items():
        ic(job_id)
        ic(queue)
        if not queue:
            continue
        if job_ready_time[job_id] <= time:
            machine, duration = queue[0]
            ready_tasks.append((duration, job_id, machine))
            ic((duration, job_id, machine))

    # Step 2: sort by SPT
    console.print("sort by SPT", style="red")
    ready_tasks.sort()
    ic(ready_tasks)

    # Step 3: schedule on available machines using LSF
    console.print("arrange jobs to progress", style="red")
    for duration, job_id, machine in ready_tasks:
        ic(duration, job_id, machine)
        m = machines[machine]
        ic(machines[machine])
        if m.available_at <= time:
            slack = due_dates[job_id] - time - job_time_remaining[job_id]
            in_progress.append((slack, job_id, machine, duration))

    # Step 4: sort by LSF and assign jobs
    console.print("sort by LSF", style="red")
    in_progress.sort()
    ic(in_progress)
    assigned_jobs = set()
    for slack, job_id, machine, duration in in_progress:
        ic(slack, job_id, machine, duration)
        ic(assigned_jobs)
        if job_id in assigned_jobs:
            continue
        m = machines[machine]
        ic(machines[machine])
        if m.available_at <= time:
            start = time
            end = time + duration
            m.timeline.append((start, end, job_id))
            m.available_at = end
            job_queues[job_id].popleft()
            job_time_remaining[job_id] -= duration
            job_ready_time[job_id] = end
            if not job_queues[job_id]:
                finished_jobs.add(job_id)
            assigned_jobs.add(job_id)
            event_log.append({
                'time': time,
                'job_id': job_id,
                'machine': machine,
                'duration': duration,
                'slack': slack,
                'action': f"投料J{job_id}到機台{machine}（派工：LSF）"
            })
            print("✅")
        else:
            print("❌")
    in_progress.clear()
    time += 1
    print(f"\n{'-'*10}\n")

ic(event_log)


# Create Gantt chart
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['tab:blue', 'tab:orange', 'tab:green',
          'tab:red', 'tab:purple', 'tab:brown']
machine_names = ['A', 'B', 'C']
yticks = []
yticklabels = []

for i, mname in enumerate(machine_names):
    m = machines[mname]
    yticks.append(i)
    yticklabels.append(f"Machine {mname}")
    for start, end, job_id in m.timeline:
        ax.barh(i, end - start, left=start,
                color=colors[job_id - 1], edgecolor='black')
        ax.text((start + end) / 2, i,
                f"J{job_id}", va='center', ha='center', color='white', fontsize=8)

ax.set_yticks(yticks)
ax.set_yticklabels(yticklabels)
ax.set_xlabel("Time")
ax.set_title("Gantt Chart: SPT(feed) + LSF(dispatch)")
plt.tight_layout()
plt.show()
