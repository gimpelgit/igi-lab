class FigureColor:
	def __init__(self, color: str):
		self.__color = color

	
	@property
	def color(self):
		return self.__color
	

	@color.setter
	def color(self, color: str):
		self.__color = color
		