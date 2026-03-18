"""
Module for determination if the string is binary number.
"""
def is_binary(string: str) -> bool:
    """
    Check if string contains only binary digits (0 and 1).

    Args:
        string: Input string to check

    Returns:
        True if string consists only of '0' and '1', False otherwise
        Empty string returns False
    """
    for char in string:
        if char not in '01':
            return False
    return True

