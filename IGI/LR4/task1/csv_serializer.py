from .serializer import Serializer
from .workload import Workload
import csv


class CsvSerializer(Serializer):
	@classmethod
	def serialize(cls, all_workloads: dict[str, list[Workload]], path: str):
		try:
			with open(path, mode='w', newline='') as file:
				writer = csv.writer(file)
				writer.writerow(['Surname', 'Name class', 'Amount hours'])
				for surname, teacher_workloads in all_workloads.items():
					for workload in teacher_workloads:
						writer.writerow([surname, workload.name_class, workload.amount_hours])
		except:
			print("There was a problem with the serialisation of the object.")


	@classmethod
	def deserialize(cls, path: str):
		all_worloads = {}
		try:
			with open(path, mode='r', newline='') as file:
				reader = csv.reader(file)
				next(reader)
				for row in reader:
					workload = Workload(row[0], row[1], int(row[2]))
					if workload.surname in all_worloads:
						all_worloads[workload.surname].append(workload)
					else:
						all_worloads[workload.surname] = [workload]
		except:
			print("There was a problem with the deserialisation of the object.")
		return all_worloads