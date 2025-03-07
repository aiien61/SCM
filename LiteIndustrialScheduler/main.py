from datetime import datetime, timedelta
from typing import List
from rich import print
import heapq
import random

class Job:
    def __init__(self, job_id: int, processing_time: float, deadline: datetime):
        self.job_id = job_id
        self.processing_time = processing_time
        self.deadline = deadline

    def __lt__(self, other):
        return self.deadline < other.deadline
    

class Scheduler:
    def __init__(self):
        self.jobs: List[Job] = []
        self.schedule: List[tuple] = []

    def add_job(self, job_id: int, processing_time: float, deadline: datetime):
        job: Job = Job(job_id, processing_time, deadline)
        heapq.heappush(self.jobs, job)
    
    def generate_schedule(self, start_time: datetime):
        current_time: datetime = start_time
        while self.jobs:
            job: Job = heapq.heappop(self.jobs)
            finish_time: datetime = current_time + timedelta(minutes=job.processing_time)
            self.schedule.append((job.job_id, current_time, finish_time))
            current_time = finish_time
    
    def display_schedule(self):
        print("Generated Schedule:")
        for job_id, start, end in self.schedule:
            start_time_str: str = start.strftime('%Y-%m-%d %H:%M')
            end_time_str: str = end.strftime('%Y-%m-%d %H:%M')
            print(f"Job {job_id}: Start at {start_time_str} - End at {end_time_str}")
    
if __name__ == "__main__":
    scheduler: Scheduler = Scheduler()
    num_jobs: int = int(input("Enter number of jobs: "))
    start_time: datetime = datetime.now() + timedelta(days=2)

    for i in range(num_jobs):
        job_id: int = i
        processing_time: int = random.randint(10, 600)
        deadline: datetime = start_time + timedelta(days=random.randint(1, 10), minutes=random.randint(1, 100))
        scheduler.add_job(job_id, processing_time, deadline)

    scheduler.generate_schedule(start_time)
    scheduler.display_schedule()
