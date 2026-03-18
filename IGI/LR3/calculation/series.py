"""
Module for calculating arcsin(x) using power series expansion.
Provides function for series approximation.
"""
from math import asin, fabs
from utils.output import *

def calculate_series(x: float, eps: float) -> float:
    """
    Calculate arcsin(x) using power series expansion.
    Series: arcsin(x) = x + (1/6)x^3 + (3/40)x^5 + ...

    Args:
        x: Input value in range [-1.0, 1.0]
        eps: Precision (stopping criterion)

    Returns:
        float: arcsin(x) approximation using series

    Note:
        Maximum 500 iterations to prevent infinite loop
    """
    series = x
    a = x
    arcsin_value = asin(x)
    for i in range(500):
        print_table(x, i, series, arcsin_value, eps)
        if fabs(arcsin_value - series) < eps:
            break
        a *= (2*i + 1)**2 * x**2 / ((2*i + 2)*(2*i + 3))
        series += a
    return series