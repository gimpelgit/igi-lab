import math
from define_task import define_task
from secure_input import secure_input


def exp_x(x: float, eps: float = 1e-5):
    """
        A function that finds e^x using a power series expansion.

        Args:
            x (float): The value of x for which the sum of the series is calculated.
            eps (float): The accuracy with which the value of e^x is to be obtained.
        
        Returns:
            float: e raised to the power of x.
            int: The number of iterations.
    """
    max_operation = 500
    n = 0
    term = 1.0
    sum = term
    while n <= max_operation and term > eps:
        n += 1
        term *= x / n
        sum += term
    return sum, n


@define_task("Задание №1. Посчитать значение функции e^x с помощью \
разложения ее в ряд Тейлора")
def task1():
    """
        The function asks the user to input x and eps values. Calculates
        the value of the function e^x with eps precision using the function
        exp_x(x, eps) and compares it with the result of the function math.exp(x).
        Displays the result on the screen.
    """
    x = secure_input(float, "Enter x: ")
    eps = secure_input(float, "Enter eps: ", lambda val: val < 1)
    f = exp_x(x, eps)
    math_f = math.exp(x)
    print("x | n | F(x) | Math F(x) | eps")
    print(f"{x} | {f[1]} | {f[0]} | {math_f} | {eps}")