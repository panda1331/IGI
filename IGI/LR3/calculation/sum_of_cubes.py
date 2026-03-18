"""
Module for calculating sum of cubes with special condition (stop on 12).
"""
from utils.input import input_int

def summary(seq:list) -> float:
    """
    Calculate sum of cubes until first 12.

    Args:
        seq: List of numbers

    Returns:
        Sum of cubes before first 12
    """
    summ = 0
    for num in seq:
        summ += num ** 3
    return summ