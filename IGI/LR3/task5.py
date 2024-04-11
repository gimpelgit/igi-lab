from secure_input import secure_input
from define_task import define_task


def generator_number(size: int):
    """
        A function that asks the user for 'size' numbers of type float.

        Args:
            size: How many numbers to request from the user?
    """
    for i in range(size):
        yield secure_input(float, "Enter number: ")


def max_abs_element(lst: list[float]):
    """
        A function that finds the maximum modulo element of the list.

        Args:
            lst: A list in which to search for the maximum modulo element.
        
        Returns:
            float: Maximum modulo element of the list.
    """
    return max(lst, key=lambda x: abs(x))


def sum_between_first_and_second_positive(lst: list[float]):
    """
        A function that finds the sum of the list elements located between
        the first and second positive elements.
        
        If the second positive element is not found it will return 0.
        
        Args:
            lst: A list in which to search for the maximum modulo element.
        
        Returns:
            float: The sum of the elements of the list located between the
            first and second positive elements.
    """
    start = -1
    end = -1
    res = 0
    for i, num in enumerate(lst):
        if num > 0:
            if start == -1:
                start = i
                continue
            else:
                end = i
                break
        if start != -1:
            res += num
    if start == -1 or end == -1:
        res = 0
    return res


@define_task("Задание №5. Найти максимальный по модулю элемент списка \
и сумму элементов списка, расположенных между первым и вторым положительными \
элементами")
def task5():
    """
        Function to perform task 5.

        Task 5 includes calling sum_between_first_and_second_positive,
        max_abs_element functions on a certain input list.
    """
    size_list = secure_input(int, "Enter list size: ", lambda x: x > 0)
    lst = list(generator_number(size_list))
    
    print(f"The maximum modulus element is equal to {max_abs_element(lst)}")
    print(f"Sum between first and second positive elements is equal to {sum_between_first_and_second_positive(lst)}")
