from secure_input import secure_input
from define_task import define_task


@define_task("Задание №2. Организовать цикл, который принимает целые \
числа с клавиатуры и подсчитывает количество неотрицательных чисел. \
Окончание цикла – ввод числа, меньшего –100")
def task2():
    """
        Function for calculation of the amount of non-negative numbers.

        The function asks the user to enter integers until a number less
        than -100 is entered. And then displays the result on the screen.
    """
    count = 0
    while True:
        val = secure_input(int, "Enter an integer. To complete, enter a number less than -100: ")
        if val < -100:
            break
        count += val >= 0
    print(f"The number of non-negative numbers among the data is {count}")
