import multiprocessing as mp
import time
import random
from dataclasses import dataclass
from typing import List, Collection, Dict
from queue import Empty
from enum import Enum, auto

class Status(Enum):
    PENDING = auto()
    IN_PROGRESS = auto()
    ON_TIME = auto()
    LATE = auto()

# Define a Job class to represent tasks
@dataclass
class Job:
    id: int
    processing_time: float
    deadline: float
    status: Status = Status.PENDING

# Machine Agent: Represents a machine that processes jobs
class MachineAgent:
    def __init__(self, id: int, queue: mp.Queue, result_queue: mp.Queue):
        self.id = id
        self.queue = queue  # Queue for receiving jbos
        self.result_queue = result_queue  # Queue for reporting completion
        self.busy_until = 0.0  # Time when machine will be free

    def process_job(self, job: Job, current_time: float):
        # Simulates job processing
        if current_time < self.busy_until:
            wait_time = self.busy_until - current_time
            time.sleep(wait_time)
            current_time = self.busy_until
        
        print(f"Machine {self.id} starting Job {job.id} at {current_time}")
        job.status = Status.IN_PROGRESS
        time.sleep(job.processing_time)  # Simulats processing
        completion_time: float = current_time + job.processing_time
        job.status = Status.ON_TIME if completion_time <= job.deadline else Status.LATE
        print(f"Machine {self.id} completed Job {job.id} at {completion_time:.2f} ({job.status})")

        # Report completion
        self.result_queue.put((job.id, completion_time, job.status))
        self.busy_until = completion_time
    
    def run(self, start_time: float):
        print(f"Machine {self.id} started")
        while True:
            try:
                # Get job from queue (timeout to allow graceful shutdown)
                job: Job = self.queue.get(timeout=1)
                current_time: float = time.time() - start_time
                self.process_job(job, current_time)
            except Empty:
                # Exit if no jobs for 1 second (simulating idle shutdown)
                print(f"Machine {self.id} shutting down (idle)")
                break
            except Exception as e:
                print(f"Machien {self.id} error: {e}")
                break
    
# Coordinator Agent: Distributes jobs and tracks progress
class CoordinatorAgent:
    def __init__(self, num_machines: int, jobs: List[Job]):
        self.jobs = jobs
        self.num_machines = num_machines
        self.job_queues: List[Collection] = [mp.Queue() for _ in range(num_machines)]
        self.result_queue: Collection[Job] = mp.Queue()
        self.completed_jobs: Dict[int, tuple] = {}

    def distribute_jobs(self):
        # Simple distributiong: assign jobs to least busy machine (round-robin for demo)
        for i, job in enumerate(self.jobs):
            machine_idx: int = i % self.num_machines
            self.job_queues[machine_idx].put(job)
            print(f"Coordinator assigned Job {job.id} to Machine {machine_idx}")
    
    def monitor_progress(self):
        jobs_remaining: int = len(self.jobs)
        while jobs_remaining > 0:
            try:
                job_id, completion_time, status = self.result_queue.get(timeout=1)
                self.completed_jobs[job_id] = (completion_time, status)
                jobs_remaining -= 1
                print(f"Coordinator: Job {job_id} completed ({status})")
            except Empty:
                continue
        
    def run(self, start_time: float):
        # Start machine agents in separate processes
        machines = [
            mp.Process(
                target=MachineAgent(i, self.job_queues[i], self.result_queue).run,
                args=(start_time,)
            )
            for i in range(self.num_machines)
        ]

        for machine in machines:
            machine.start()
        
        # Distribute jobs
        self.distribute_jobs()

        # Monitor progress
        self.monitor_progress()

        # Cleanup
        for machine in machines:
            machine.join()

        print("\nSummary:")
        for job_id, (completion_time, status) in self.completed_jobs.items():
            print(f"Job {job_id}: Completed at {completion_time:.2f} ({status})")

# Demo setup
def create_sample_jobs(num_jobs: int) -> List[Job]:
    return [Job(id=i, processing_time=random.uniform(0.5, 2.0), deadline=5+i) for i in range(num_jobs)]

if __name__ == "__main__":
    # Record start time for relative timing
    start_time = time.time()

    # Parameters
    NUM_MACHINES: int = 3
    NUM_JOBS: int = 6

    # Create sample jobs
    jobs: List[Job] = create_sample_jobs(NUM_JOBS)
    print("Jobs created:", [(j.id, j.processing_time, j.deadline) for j in jobs])

    # Initialise and run coordinator
    coordinator = CoordinatorAgent(NUM_MACHINES, jobs)
    coordinator.run(start_time)