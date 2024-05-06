from abc import ABC, abstractmethod
from .workload import Workload


class Serializer(ABC):
	@classmethod 
	@abstractmethod
	def serialize(cls, workloads: dict[str, Workload], path: str):
		pass

	@classmethod 
	@abstractmethod
	def deserialize(cls, path: str):
		pass

