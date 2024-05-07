from utils.secure_input import secure_input
from .taylor_exp import taylor_exp
from .save_graph import save_graph
import math
import numpy
import statistics


def task3():
	x = secure_input(float, "Enter x: ")
	n = secure_input(int, "Enter n: ", lambda val: val > 1)
	f, arr = taylor_exp(x, n, True)
	math_f = math.exp(x)
	print("x | n | F(x) | Math F(x) | eps")
	print(f"{x} | {n} | {f} | {math_f} | {math.fabs(f - math_f)}")
	print(f"average: {statistics.mean(arr)}")
	print(f"median: {statistics.median(arr)}")
	print(f"mode: {statistics.mode(arr)}")
	print(f"variance: {statistics.variance(arr)}")
	print(f"standard deviation: {statistics.stdev(arr)}")
	
	x = numpy.arange(-1, 1, 0.05)
	y1 = [taylor_exp(xi, n) for xi in x]
	y2 = [math.exp(xi) for xi in x]
	save_graph("task3/graph.png", x, y1, x, y2)