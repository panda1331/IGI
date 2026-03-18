"""
Task 2: Calculate sum of cubes with stop condition.

Program calculates sum of cubes of entered numbers.
Input stops if value equals 12.
User chooses between manual input and random generation.

Input: n (number of elements)
Output: Sum of cubes (excluding 12 itself)

Lab 3: Standard data types, collections, functions, modules
Python 3.12.3
Developer: Morozova E.S.
Date: 09.03.2026
"""
from calculation.sum_of_cubes import summary
from utils.input import input_int, enter_sequence_float_with_required_num
from utils.output import print_choice_task2, show_task2
from utils.generator import generate_sequence_float


def task2():
    """Execute task 2."""
    show_task2()
    seq = []
    seq_size = input_int(1, 100, "Enter n: ")
    print_choice_task2()
    choice = input_int(1, 2, "Enter choice: ")
    match choice:
        case 1:
            seq = generate_sequence_float(seq, seq_size)
            print(f"Generated sequence: {seq}")
        case 2:
            try:
                seq = enter_sequence_float_with_required_num(seq, seq_size, 12.0)
                print(f"Entered sequence: {seq}")
            except ValueError as e:
                print(e)
                return
    print(f"Result: {summary(seq)}")