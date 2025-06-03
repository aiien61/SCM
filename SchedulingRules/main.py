from collections import deque, defaultdict
from icecream import ic
from dataclasses import dataclass
from enum import Enum
from rich.console import Console
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt

console = Console()

# Job data: list of tasks per job in the form (machine, duration)
orders: Dict[int, list] = {
    1: [('A', 3), ('B', 3), ('C', 2)],
    2: [('A', 5), ('C', 2)],
    3: [('B', 4), ('A', 4), ('C', 3)],
    4: [('B', 3), ('C', 5), ('A', 2)],
    5: [('C', 5), ('B', 4)],
    6: [('C', 2), ('A', 5), ('B', 5)],
}

# Due dates
orders_due: Dict[int, int] = {
    1: 10,
    2: 13,
    3: 12,
    4: 18,
    5: 14,
    6: 15,
}

# Simulate scheduling with SPT (投料) and LSF (派工)

class Status(Enum):
    PENDINGD = "Pending"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

class Machine:
    def __init__(self, type_: str):
        self.type = type_
        self.timeline = []  # (start, end, job_id)
        self.available_at = 0

    def __str__(self):
        return f"{self.type}(timeline={self.timeline}, available_at={self.available_at})"

    def __repr__(self):
        return str(self)

@dataclass
class Job:
    order_id: int
    status: Status
    machine: Optional[str]
    duration: int

makespan: Dict[int, int] = {}
for mo, jobs in orders.items():
    makespan[mo] = sum(d for _, d in jobs)

jobs: List[Job] = []
for mo in orders.keys():
    machine, duration = orders[mo].pop(0)
    jobs.append(Job(mo, Status.PENDINGD, machine, duration))

# Re-simulate to extract detailed step-by-step 投料與派工紀錄
machines = {'A': Machine(type_="A"),
            'B': Machine(type_="B"),
            'C': Machine(type_="C")}

agent: Dict[int, int] = {}

time = 0
in_progress = []
finished_jobs = set()
event_log = []

while jobs:
    ic(time)
    ic(finished_jobs)
    ic(jobs)

    # Step 1: collect ready tasks (SPT投料)
    console.print("collect ready tasks", style="red")
    ready_tasks = []
    for job in jobs:
        ic(job)
        if job.status == Status.IN_PROGRESS:
            if agent[job.order_id] == time:
                match job.machine:
                    case None: job.status = Status.DONE
                    case _: job.status = Status.PENDINGD

        if job.status == Status.PENDINGD:
            ready_tasks.append(job)

        if job.status == Status.DONE:
            finished_jobs.add(job.order_id)

    # Step 2: sort by SPT
    console.print("sort by SPT", style="red")
    ready_tasks.sort(key=lambda x: x.duration)
    ic(ready_tasks)

    # Step 3: schedule on available machines using LSF
    console.print("arrange jobs to progress", style="red")
    for job in ready_tasks:
        ic(job)
        m = machines[job.machine]
        ic(machines[machine])
        if m.available_at <= time:
            slack = orders_due[job.order_id] - time - makespan[job.order_id]
            in_progress.append((job, slack))

    # Step 4: sort by LSF and assign jobs
    console.print("sort by LSF", style="red")
    in_progress.sort(key=lambda x: x[1])
    ic(in_progress)
    assigned_jobs = set()
    for job, slack in in_progress:
        ic(job, slack)
        ic(assigned_jobs)
        if job.order_id in assigned_jobs:
            continue
        m = machines[machine]
        ic(machines[machine])
        if m.available_at <= time:
            start = time
            end = time + job.duration
            m.timeline.append((start, end, job.order_id))
            m.available_at = end
            makespan[job.order_id] -= duration
            
            agent[job.order_id] = end            
            assigned_jobs.add(job.order_id)
            machine, duration = orders[job.order_id].pop(0) if orders[job.order_id] else (None, 0)

            job.machine = machine
            job.duration = duration
            job.status = Status.IN_PROGRESS
            
            event_log.append({
                'time': time,
                'job_id': job.order_id,
                'machine': machine,
                'duration': duration,
                'slack': slack,
                'action': f"投料J{job.order_id}到機台{machine}（派工：LSF）"
            })
            print("✅")
        else:
            print("❌")
    
    in_progress.clear()
    time += 1
    print(f"\n{'-'*10}\n")

ic(event_log)
