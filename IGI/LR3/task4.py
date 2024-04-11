from define_task import define_task


def count_min_words(text):
    """
        A function that determines how many words in the text have a minimum length.

        Args:
            text (str): Input text
        
        Returns:
            int: Number of words with minimum length.
    """
    text = text.replace(',', '')
    words = text.split()
    min_length = len(min(words, key=len))
    count = len(list(filter(lambda word: len(word) == min_length, words)))
    return count


def get_all_words_followed_by_comma(text):
    """
        A function that finds all words followed by a comma in the text.

        Args:
            text (str): Input text
        
        Returns:
            list[str]: Words followed by a comma.
    """
    words = text.split()
    lst = list(filter(lambda word: word[-1] == ',', words))
    lst = list(map(lambda word: word.rstrip(','), lst))
    return lst


def get_all_min_words_that_end_symbol(text, symbol):
    """
        A function that finds the longest word in the text ending with
        the given character.

        Args:
            text (str): Input text
            symbol (str): What symbol should the words end with?
        
        Returns:
            list[str]: Words followed by a symbol.
    """
    text = text.replace(',', '')
    words = text.split()
    words_end_symbol = list(filter(lambda word: word[-1] == symbol, words))
    min_length = len(min(words_end_symbol, key=len))
    return list(filter(lambda word: len(word) == min_length, words_end_symbol))


@define_task("Задание №4.\n\
а) определить, сколько слов имеют минимальную длину;\n\
б) вывести все слова, за которыми следует запятая;\n\
в) найти самое длинное слово, которое заканчивается на 'y'")
def task4():
    """
        Function to perform task 4.

        Task 4 includes calling get_all_words_followed_by_comma,
        count_min_words, get_all_min_words_that_end_symbol functions
        on a certain input text.
    """
    text = "So she was considering in her own mind, as well as she could, for the hot day made her feel"\
    "very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble"\
    "of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."

    print(f"{count_min_words(text)} words have a minimum length")
    print(f"All words followed by a comma: {get_all_words_followed_by_comma(text)}")
    print(f"Words that end in 'y': {get_all_min_words_that_end_symbol(text, 'y')}")
