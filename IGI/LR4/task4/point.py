from math import sqrt


class Point:
	def __init__(self, x, y):
		self.__x = x
		self.__y = y

	@property
	def x(self):
		return self.__x
	
	
	@x.setter
	def x(self, x):
		self.__x = x

	
	@property
	def y(self):
		return self.__y
	
	
	@y.setter
	def y(self, y):
		self.__y = y


	def distance(self, other):
		return sqrt((self.__x - other.__x)**2 + (self.__y - other.__y)**2)