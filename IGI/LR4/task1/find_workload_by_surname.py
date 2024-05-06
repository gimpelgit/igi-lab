from .workload import Workload


def find_workload_by_surname(all_workloads: dict[str, list[Workload]], surname: str):
	if surname in all_workloads:
		return sum(workload.amount_hours for workload in all_workloads[surname])
	return 0