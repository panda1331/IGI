"""
Module for input validation and sequence initialization.
Provides functions for safe user input with type checking and range validation.
"""

def input_int(min_value: int, max_value: int, message: str) -> int:
    """Input integer number from min to max."""
    while True:
        try:
            value = int(input(message))
            if min_value <= value <= max_value:
                return value
            else:
                print("Invalid value. Please try again.")
                continue

        except ValueError:
            print("Invalid value. Please try again.")
            continue

def input_float(min_value: float, max_value: float, message: str) -> float | None:
    """Input float number from min to max."""
    while True:
        try:
            value = float(input(message))
            if min_value < value < max_value:
                return value
            else:
                continue
        except ValueError:
            print("Invalid value. Please try again.")

def input_str(message: str) -> str | None:
    """Input string."""
    while True:
        try:
            value = input(message)
            if value != "":
                return value
            else:
                continue
        except ValueError:
            print("Invalid value. Please try again.")

def enter_sequence_float_with_required_num(seq: list, n: int, num: float) -> list:
    """Enter a sequence with number 12 required."""
    if n == 1:
        return seq

    is_num_in_seq = False
    for i in range(n):
        member = input_float(-1000, 1000, "Enter a number: ")
        if member == num:
            is_num_in_seq = True
            break
        seq.append(member)

    if not is_num_in_seq:
        raise ValueError(f"Error: Number {num} is not in the sequence.")
    return seq

def enter_sequence_float(seq: list, n: int) -> list:
    """Enter a sequence."""
    for i in range(n):
        member = input_float(-1000, 1000, "Enter a number: ")
        seq.append(member)
    return seq