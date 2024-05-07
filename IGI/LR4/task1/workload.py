class Workload:
	def __init__(self, surname, name_class, amount_hours):
		self.surname = surname
		self.name_class = name_class
		self.amount_hours = amount_hours

	def __str__(self):
		return f"Workload({self.surname},{self.name_class},{self.amount_hours})"
	
	def __repr__(self):
		return self.__str__()
	