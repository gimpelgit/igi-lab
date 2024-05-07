from .csv_serializer import CsvSerializer
from .pickle_serializer import PickleSerializer
from .workload import Workload
from .serializer import Serializer
from .find_workload_by_surname import find_workload_by_surname
from utils.secure_input import secure_input
from pprint import pprint


def task1():
	all_workloads = {
		"Fedu": [Workload("Fedu", "11", 50), Workload("Fedu", "7", 40)],
		"Kirill": [Workload("Kirill", "9", 60)],
		"Sveta": [Workload("Sveta", "10A", 100)],
	}
	choice = secure_input(int, "Enter the serialisation method (1 - csv, 2 - pickle): ", lambda x: 1 <= x <= 2)
	serializer: Serializer
	match choice:
		case 1:
			path = "task1/task1.csv"
			serializer = CsvSerializer
		case 2:
			path = "task1/task1.pickle"
			serializer = PickleSerializer

	serializer.serialize(all_workloads, path)
	loaded_workloads = serializer.deserialize(path)
	print("Full school workload")
	pprint(loaded_workloads)
	surname = input("Enter the instructor's last name to find out their workload: ")
	print("Teacher workload:", find_workload_by_surname(loaded_workloads, surname))
