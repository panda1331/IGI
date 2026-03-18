"""
Module for float list operations in Task 5.
"""

def calculate_amount_of_nums_bigger_than_c(seq:list, c: float) -> int:
    """
    Count the number of elements in sequence greater than given value c.

    Args:
        seq: List of numbers (can be int or float)
        c: Threshold value to compare against

    Returns:
        int: Count of elements where element > c
    """
    return sum(1 for i in seq if i > c)

def calculate_product_of_nums(seq:list) -> float:
    """
    Multiply elements before max absolute value.

    Args:
        seq: List of numbers

    Returns:
        Product of elements before first occurrence of max abs value
    """
    max_index = seq.index(max(seq, key=abs))
    product = 1
    for i in range(max_index):
        product *= seq[i]
    return product