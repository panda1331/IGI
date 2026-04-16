"""
Module for input validation and sequence initialization.
Provides functions for safe user input with type checking and range validation.
"""
from utils.constants import ALLOWED_COLORS, DEFAULT_COLOR

def input_int(min_value: int, max_value: int, message: str) -> int | None:
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

def input_float(min_value: float, max_value: float, message: str, including: bool = False) -> float | None:
    """Input float number from min to max."""
    while True:
        try:
            value = float(input(message))
            if including:
                if min_value <= value <= max_value:
                    return value
                else:
                 continue
            else:
                if min_value < value < max_value:
                    return value
                else:
                    continue
        except ValueError:
            print("Invalid value. Please try again.")

def check_color(allowed_colors: list):
    print("Available colors:", end=" ")
    for index, color in enumerate(allowed_colors):
        if index == len(allowed_colors) - 1:
            print(color)
        else:
            print(color, end=", ")
    color = input_str("Enter color: ").lower()
    if color not in ALLOWED_COLORS:
        print(f"\n!!! Invalid color. Default color is {DEFAULT_COLOR}. !!!")
        color = DEFAULT_COLOR
    return color

