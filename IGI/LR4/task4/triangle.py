from .geometric_figure import GeometricFigure
from .point import Point
from .figure_color import FigureColor
from .nameable_figure import NameableFigure
import matplotlib.pyplot as plt
import math


class Triangle(NameableFigure, GeometricFigure):
	def __init__(self, side, angleB, angleC, color, start = Point(1, 1)):
		super().__init__("Triangle")
		self.__color = FigureColor(color)
		self.__start = start
		self.__B = Point(start.x, start.y)
		self.__C = Point(start.x + side, start.y)
		AC = side * math.sin(math.radians(angleB)) / math.sin(math.radians(180 - angleB - angleC))
		self.__A = Point(self.__C.x - AC * math.cos(math.radians(angleC)),
                     self.__C.y + AC * math.sin(math.radians(angleC)))


	def save_and_show(self, path: str, description: str):
		x = [self.__A.x, self.__B.x, self.__C.x, self.__A.x]
		y = [self.__A.y, self.__B.y, self.__C.y, self.__A.y]
		plt.plot(x, y, label=description, color=self.__color.color)
		plt.legend()
		plt.fill(x, y, color=self.__color.color)
		plt.axis('equal')
		plt.ylim(self.__start.y - 1, self.__A.y + 1)
		plt.savefig(path)
		plt.show()


	def area(self):
		return math.fabs(0.5*(self.__A.x*(self.__B.y - self.__C.y) + 
													self.__B.x*(self.__C.y - self.__A.y) + 
													self.__C.x*(self.__A.y - self.__B.y)))
	
	def __str__(self):
		return '''
Figure: {}
Side AC = {:.5f} 
Side AB = {:.5f} 
Side BC = {:.5f}
Point A = ({:.5f}, {:.5f}) 
Point B = ({:.5f}, {:.5f}) 
Point C = ({:.5f}, {:.5f})
Area S = {:.5f} 
		'''.format(
			self.name,
			self.__A.distance(self.__C),
			self.__A.distance(self.__B),
			self.__B.distance(self.__C),
			self.__A.x, self.__A.y,
			self.__B.x, self.__B.y,
			self.__C.x, self.__C.y,
			self.area()
		)