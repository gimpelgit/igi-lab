from .triangle import Triangle
from utils.secure_input import secure_input


def task4():
	side = secure_input(float, "Enter a side: ", lambda x: x > 0)
	angleB = secure_input(float, "Enter angle B: ", lambda x: 0 < x < 180)
	angleC = secure_input(float, "Enter angle C: ", lambda x: 0 < x < 180 - angleB)
	colors = {'r', 'b', 'c', 'g', 'm', 'y', 'k'}
	print("Acceptable colors:", colors)
	color = secure_input(str, "Enter a color: ", lambda x: x in colors)
	description = secure_input(str, "Enter description: ", lambda x: len(x) > 0)
	triangle = Triangle(side, angleB, angleC, color)
	print(str(triangle))
	triangle.save_and_show("task4/graph.png", description)
