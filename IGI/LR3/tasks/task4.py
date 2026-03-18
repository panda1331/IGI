"""
Task 4: Text Analysis.

Program analyzes given text and performs three operations:
a) Count lowercase letters.
b) Find the last word containing letter 'i' and its position.
c) Display text excluding words starting with 'i'.

Input: Predefined text string.
Output: Analysis results and modified text.

Lab 3: Standard data types, collections, functions, modules.
Python 3.12.3.
Developer: Morozova E.S.
Date: 09.03.2026.
"""
from calculation.string_operations import calculate_lowercase_letters, find_last_word_ends_with_i, \
    delete_words_start_with_i
from utils.output import show_task4


def task4():
    """Execute task 4."""
    show_task4()
    input_string = "So she was considering spaghetti in her own mind, as well as she could, for sushi the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit kiwi with pink eyes ran close by her.\n"
    print(input_string)
    print(f"a) Amount of lowercase letters: {calculate_lowercase_letters(input_string)}")
    last_word = find_last_word_ends_with_i(input_string)
    print(f"b) Last word that ends with 'i': {last_word[0]} at position: {last_word[1]}")
    print(f"c) String without words start with 'i': \n{delete_words_start_with_i(input_string)}")