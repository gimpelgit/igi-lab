# Lab: 4
# Author: Gimpel Kirill
# Date: 06.05.2024
# Version: 1.0

from task1.task1 import task1
from task2.task2 import task2
from task3.task3 import task3
from task4.task4 import task4
from task5.task5 import task5
from utils.secure_input import secure_input


if __name__ == '__main__':
	while True:
		choice = secure_input(int, "Enter task number or press 0 to exit: ", lambda x: 0 <= x <= 5)
		match choice:
			case 0:
				break
			case 1:
				task1()
			case 2:
				task2()
			case 3:
				task3()
			case 4:
				task4()
			case 5:
				task5()