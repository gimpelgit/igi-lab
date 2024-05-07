from .matrix_worker import MatrixWorker


def task5():
	worker = MatrixWorker(1, 100)
	print(worker.matrix)
	print("\nAfter sorting the last row")
	worker.sort_last_row()
	print(worker.matrix)
	print("\nMedian:", worker.median_last_row())
	print("Median (numpy):", worker.median_last_row_numpy())