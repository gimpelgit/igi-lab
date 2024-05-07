import numpy as np


class MatrixWorker:
	def __init__(self, low: int, high: int):
		size = np.random.randint(1, 11, size=2)
		self.__matrix = np.random.randint(low, high, size=size)


	@property
	def matrix(self):
		return self.__matrix


	def sort_last_row(self):
		self.__matrix[-1] = np.sort(self.__matrix[-1])


	def median_last_row(self):
		is_sorted = np.all(np.diff(self.__matrix[-1]) >= 0)
		
		if not is_sorted:
			row = np.sort(self.__matrix[-1])
		else:
			row = self.__matrix[-1]
		mid = (row.size - 1) // 2
		if row.size % 2 == 1:
			return row[mid]
		return (row[mid] + row[mid + 1]) / 2
	

	def median_last_row_numpy(self):
		return np.median(self.__matrix[-1])