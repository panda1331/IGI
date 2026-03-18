"""
Task 5: Float list operations.

Input: n, sequence of n floats, threshold c.
Output: count > c and product before max abs.

Lab 3.
Developer: Morozova E.S.
Date: 09.03.2026.
"""

from calculation.float_list_operations import calculate_amount_of_nums_bigger_than_c, calculate_product_of_nums
from utils.input import input_int, enter_sequence_float, input_float
from utils.output import show_task5


def task5():
    """Execute task 5."""
    show_task5()
    seq = []
    seq_size = input_int(1, 100, "Enter a n: ")
    seq = enter_sequence_float(seq, seq_size)
    c_param = input_float(-1000, 1000, "Enter a c: ")
    print(f"1. Amount of nums that are bigger than {c_param}: {calculate_amount_of_nums_bigger_than_c(seq, c_param)}")
    print(f"2. Product of numbers before maximum absolute value: {calculate_product_of_nums(seq)}")