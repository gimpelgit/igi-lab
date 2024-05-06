from .serializer import Serializer
from .workload import Workload
import pickle


class PickleSerializer(Serializer):
	@classmethod
	def serialize(cls, all_workloads: dict[str, list[Workload]], path: str):
		try:
			with open(path, mode='wb') as file:
				pickle.dump(all_workloads, file)
		except:
			print("There was a problem with the serialisation of the object.")


	@classmethod
	def deserialize(cls, path: str):
		all_worloads = {}
		try:
			with open(path, mode='rb') as file:
				all_worloads = pickle.load(file)
		except:
			print("There was a problem with the deserialisation of the object.")
		return all_worloads