"""
Module for string operations in Task 4.
Provides functions for text analysis: counting lowercase letters,
finding words ending with 'i', and deleting words starting with 'i'.
"""
import string

def calculate_lowercase_letters(s: str) -> int:
    """
    Count the number of lowercase letters in a string.

    Args:
        s: Input string to analyze

    Returns:
        int: Total count of lowercase characters (a-z)
    """
    letters = list(s)
    lowercase_letters = [letter for letter in letters if letter.islower()]
    return len(lowercase_letters)

def find_last_word_ends_with_i(s: str) -> tuple:
    """
    Find the last word in text that ends with letter 'i' (case-insensitive).

    Args:
        s: Input text to search through

    Returns:
        tuple: (word, position) where:
            - word: the last word ending with 'i' (without punctuation)
            - position: index of this word in the original text
            Returns (None, -1) if no such word found
    """
    words_end_with_i = []
    words = s.split()
    positions = []
    for i, word in enumerate(words):
        clean_word = word.strip(string.punctuation)
        if clean_word and clean_word[-1].lower() == 'i':
            words_end_with_i.append(clean_word)
            positions.append(i)
    if words_end_with_i:
        return words_end_with_i[-1], positions[-1]
    else:
        return None, -1

def delete_words_start_with_i(s: str) -> str:
    """
    Delete all words that start with letter 'i' (case-insensitive).

    Args:
        s: Input text to process

    Returns:
        str: New string with all words starting with 'i' removed
             Words are joined with single spaces
    """
    words = s.split()
    new_s = []
    for word in words:
        clean_word = word.strip(string.punctuation)
        if clean_word and clean_word[0].lower() != 'i':
            new_s.append(word)
        elif not clean_word:
            new_s.append(word)
    return ' '.join(new_s)