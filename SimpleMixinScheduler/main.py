from datetime import datetime
from enum import Enum

from rich import print

class TaskName(Enum):
    PROCESS_ORDERS = "Process orders"
    FAILING_TASK = "Failing task"


class LoggingMixin:
    def log(self, message: str):
        print(f"[{datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}] {message}")


class RetryMixin:
    def __init__(self, max_retries: int=3, *args, **kwargs):
        self.max_retries = max_retries
        self.retries: int = 0
        super().__init__(*args, **kwargs)

    def retry(self) -> bool:
        if self.retries < self.max_retries:
            self.retries += 1
            self.log(f"Retrying task (attempt {self.retries})...")
            return True
        else:
            self.log("Max retries reached. Task failed.")
            return False


class PriorityMixin:
    def __init__(self, priority: int=1, *args, **kwargs):
        self.priority = priority
        super().__init__(*args, **kwargs)
    
    def get_priority(self):
        return self.priority


class Task(LoggingMixin, RetryMixin, PriorityMixin):
    def __init__(self, name: TaskName, priority: int = 1, max_retries: int = 3):
        self.name = name
        super().__init__(priority=priority, max_retries=max_retries)
    
    def execute(self):
        self.log(f"Executing task: {self.name}")
        if self.name == TaskName.FAILING_TASK:
            if self.retry():
                # Retry the task
                self.execute()
        else:
            self.log(f"Task {self.name} completed successfully.")

# Example usage
task1 = Task(TaskName.PROCESS_ORDERS, priority=2)
task1.execute()

task2 = Task(TaskName.FAILING_TASK, priority=1, max_retries=2)
task2.execute()