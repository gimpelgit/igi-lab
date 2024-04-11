from secure_input import secure_input
from define_task import define_task


@define_task("Задание №3. В строке, вводимой с клавиатуры, подсчитать \
количество слов, начинающихся со строчной буквы")
def task3():
    """
        Function to perform task 3.
        
        Task 3: In the string entered from the keyboard, count the number
        of words beginning with a lowercase letter.
    """
    source_string = input("Enter the string: ")
    words = source_string.split()
    lowercase_count = 0
    for word in words:
        lowercase_count += word[0].islower()
    print(f"The number of words that begin with a lowercase letter is equal to {lowercase_count}")
