from typing import Callable


def secure_input(data_type: type, message: str, func: Callable[[type], bool] = None) -> type:
    """
        This function ensures the user inputs data of the correct type.
        If the user inputs data of the wrong type, it will keep prompting
        the user for input until they input data of the correct type.

        Args:
            data_type (type): The type of the data that the user is supposed to input.
            message (str): The message that is displayed to the user when prompting for input.
            func (function, optional): If this function returns False, the user will be prompted
            for input again. 

        Returns:
            data_type: The user's input, converted to the specified data type.
    """
    again = True
    while again:
        try:
            data = data_type(input(message))
            again = not func(data) if func else False
        except ValueError:
            pass
        if again:
            print("Incorrect input!!!")
    return data
