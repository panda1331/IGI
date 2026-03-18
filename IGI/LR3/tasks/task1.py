"""
Task 1: Calculate arcsin(x) using power series expansion.

Input: x (float in [-1.0, 1.0]), eps (float in [0.0, 1.0])
Output: Table showing iteration number, series value, math value, and precision
Iterations limited to 500

Lab 3: Standard data types, collections, functions, modules
Python 3.12.3
Developer: Morozova E.S.
Date: 09.03.2026
"""

from utils.input import *
from calculation.series import *
from utils.decorator import *

@timer_decorator
def task1():
    """Execute task 1."""
    show_task1()
    x = input_float(-1.0, 1.0, "Enter x: ")
    eps = input_float(0.0, 1.0, "Enter eps: ")
    calculate_series(x, eps)