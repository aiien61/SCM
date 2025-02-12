from enum import Enum
from typing import List, Dict
from dataclasses import dataclass

class ProcessType(Enum):
    ORDER = "order"
    CUT = "cut"
    TOPPING = "topping"
    BAKE = "bake"
    PACKAGE = "package"

@dataclass
class Process:
    type_: ProcessType
    duration: float  # in seconds

class ProductionLine:
    def __init__(self, name: str):
        self.name = name
        self.processes: List[Process] = []

    def add_process(self, process: Process) -> None:
        self.processes.append(process)

    def get_total_duration(self) -> float:
        return sum(process.duration for process in self.processes)
    
class ProductionSystem:
    def __init__(self):
        self.production_lines: List[ProductionLine] = []
        self.resources: Dict[ProcessType, int] = {
            ProcessType.BAKE: 2,  # 2 pieces of baking machines
            ProcessType.CUT: 2,
            ProcessType.TOPPING: 2
        }
    
    def add_production_line(self, line: ProductionLine):
        self.production_lines.append(line)
    
    def calculate_system_cycle_time(self) -> float:
        # Find the maximum time among all processes considering shared resources
        max_time: int = 0
        for process_type in ProcessType:
            total_time: int = 0
            processes: List[Process] = []
            for line in self.production_lines:
                matching_processes = [p for p in line.processes if p.type_ == process_type]
                processes.extend(matching_processes)
            
            if processes:
                # Calculate effective time considering parallel processing
                if process_type in self.resources:
                    num_resources = self.resources[process_type]
                    total_time = max(p.duration for p in processes)
                    # Adjust time based on available resources
                    total_time = total_time / num_resources
                else:
                    total_time = max(p.duration for p in processes)

                max_time = max(max_time, total_time)

        return max_time
    
    def calculate_hourly_production(self) -> float:
        cycle_time = self.calculate_system_cycle_time()
        seconds_per_hour = 3_600
        return seconds_per_hour / cycle_time
    
    def calculate_total_production_time(self) -> float:
        # Calculate the maximum total time among all production lines
        return max(line.get_total_duration() for line in self.production_lines)
    
def main():
    # Create the production system
    system = ProductionSystem()

    for i in range(2):
        line = ProductionLine(f"Line {i+1}")

        # Add processes with their duration
        line.add_process(Process(ProcessType.ORDER, 30))
        line.add_process(Process(ProcessType.CUT, 15))
        line.add_process(Process(ProcessType.TOPPING, 20))
        line.add_process(Process(ProcessType.BAKE, 40))
        line.add_process(Process(ProcessType.PACKAGE, 37.5))

        system.add_production_line(line)
    
    # Calculate and display results
    cycle_time = system.calculate_system_cycle_time()
    hourly_production = system.calculate_hourly_production()
    total_time = system.calculate_total_production_time()

    print(f"System cycle time: {cycle_time} seconds")
    print(f"Hourly production capacity: {hourly_production:.2f} units")
    print(f"Total production time per unit: {total_time} seconds")

if __name__ == "__main__":
    main()
