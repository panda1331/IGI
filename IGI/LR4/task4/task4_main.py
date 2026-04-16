"""
Lab work 4. File work, classes, serializers, regular expressions, standard libraries.
Task 4. Geometry figures drawing.
Version 1.0
Developer: Morozova E.S.
Date: 12.04.2026
"""
from task4.parallelogram import Parallelogram
from utils.constants import ALLOWED_COLORS
from utils.input import input_float, check_color, input_str
from utils.output import task4_info

def run():
    """Execute task 4. """
    try:
        task4_info()
        caption = input_str("Enter figure caption: ")
        diagonal1 = input_float(0, 10000, "Enter diagonal 1: ")
        diagonal2 = input_float(0, 10000, "Enter diagonal 2: ")
        angle = input_float(0, 180, "Enter angle(0° < x < 180°): ")
        color = check_color(ALLOWED_COLORS)
        parallelogram = Parallelogram(diagonal1, diagonal2, angle, color)
        print(Parallelogram.get_name())
        print(parallelogram.get_info())

        parallelogram.draw(caption)
    except FileNotFoundError as e:
        print(f"File not found error: {e}")
    except PermissionError as e:
        print(f"Permission error: {e}")
    except ValueError as e:
        print(f"Value error empty array: {e}")

