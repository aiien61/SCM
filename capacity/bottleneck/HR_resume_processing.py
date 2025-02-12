from enum import Enum
from typing import List, Dict
from dataclasses import dataclass

class ApplicantType(Enum):
    CONSULTANT = "Consultant"
    STAFF = "Staff"
    INTERNSHIP = "internship"

class ProcessStep(Enum):
    DATA_ENTRY = "Data Entry"
    CONTACT_OTHERS = "Contact Others"
    CONTACT_PREV_EMPLOYER = "Contact Previous Employer"
    PERFORMANCE_ANALYSIS = "Performance Analysis"
    SEND_CONFIRMATION = "Send Confirmation"

@dataclass
class ProcessConfig:
    time_minutes: int
    workers: int

    @property
    def hourly_capacity(self) -> int:
        return int(60 / self.time_minutes * self.workers)
    
# @dataclass
# class DemandConfig:
#     consultant: int = 0
#     staff: int = 0
#     intership: int = 0

class ProcessStep:
    def __init__(self, name: str, config: ProcessConfig):
        self.name = name
        self.config = config
        self.demand_by_type: Dict[ApplicantType, int] = {}

    def set_demand(self, applicant_type: ApplicantType, count: int):
        self.demand_by_type[applicant_type] = count

    @property
    def total_demand(self) -> int:
        return sum(self.demand_by_type.values())

    @property
    def capacity_utilization(self) -> float:
        return self.total_demand / self.config.hourly_capacity
    
class ResumeProcessSystem:
    def __init__(self):
        self.steps: Dict[str, ProcessStep] = {}
        self.initialize_steps()
    
    def initialize_steps(self):
        # Initilialize process steps with their configurations from the table
        self.steps["data_entry"] = ProcessStep("Data Entry", ProcessConfig(time_minutes=3, workers=1))
        self.steps["contact_others"] = ProcessStep("Contact Others", ProcessConfig(time_minutes=20, workers=2))
        self.steps["contact_prev_employer"] = ProcessStep("Contact Previous Employer", ProcessConfig(time_minutes=15, workers=3))
        self.steps["performance_analysis"] = ProcessStep("Performance Analysis", ProcessConfig(time_minutes=8, workers=2))
        self.steps["send_confirmation"] = ProcessStep("Send Confirmation", ProcessConfig(time_minutes=2, workers=1))

    def set_daily_demand(self, consultant: int, staff: int, internship: int) -> None:
        # Set demand for each step based on applicant type
        for step in self.steps.values():
            if step.name == "Data Entry":
                step.set_demand(ApplicantType.CONSULTANT, consultant)
                step.set_demand(ApplicantType.STAFF, staff)
                step.set_demand(ApplicantType.INTERNSHIP, internship)
            elif step.name == "Contact Others":
                step.set_demand(ApplicantType.CONSULTANT, consultant)
            elif step.name == "Contact Previous Employer":
                step.set_demand(ApplicantType.CONSULTANT, consultant)
                step.set_demand(ApplicantType.STAFF, staff)
            elif step.name == "Performance Analysis":
                step.set_demand(ApplicantType.INTERNSHIP, internship)
            elif step.name == "Send Confirmation":
                step.set_demand(ApplicantType.CONSULTANT, consultant)
                step.set_demand(ApplicantType.STAFF, staff)
                step.set_demand(ApplicantType.INTERNSHIP, internship)

    def analyze_capacity(self):
        results = []
        for step in self.steps.values():
            capacity = step.config.hourly_capacity
            demand = step.total_demand
            utilization = step.capacity_utilization

            results.append({
                "step": step.name,
                "capacity_per_hour": capacity,
                "total_demand": demand,
                "utilization": utilization,
                "is_bottleneck": utilization > 1.0
            })

        return results

def main():
    # Create system instance
    system = ResumeProcessSystem()

    # Set daily demand (e.g. 30 consultants, 110 staff, 40 internship)
    # Converting to hourly rates for 10-hour workday
    system.set_daily_demand(
        consultant=3,
        staff=11,
        internship=4
    )

    # Analyze and print results
    results = system.analyze_capacity()

    print("Resume Processing System Analysis")
    print("-" * 50)
    for result in results:
        print(f"\nProcess Step: {result['step']}")
        print(f"Hourly Capacity: {result['capacity_per_hour']}")
        print(f"Total Hourly Demand: {result['total_demand']}")
        print(f"Capacity Utitlization: {result['utilization']:.1%}")
        if result['is_bottleneck']:
            print("⚠️ This step is a bottleneck!")

if __name__ == "__main__":
    main()
