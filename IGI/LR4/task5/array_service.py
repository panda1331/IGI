"""
Task 5. Module for Array Service.
"""
import numpy as np
from task5.array_creator_mixin import ArrayCreatorMixin
from task5.array_demo_mixin import ArrayDemoMixin

class ArrayService(ArrayCreatorMixin, ArrayDemoMixin):
    """
    Main service for NumPy operations.
    Inherits array creation and demonstration methods from mixins.
    """
    def calculate_sum_of_abs_negative_numbers(self, matrix):
        """
        Calculate sum of absolute values of negative odd elements.

        Args:
            matrix: Input NumPy array

        Returns:
            float: Sum of absolute values
        """
        elements = self._select_odd_negative_nums(matrix)
        return np.sum(np.abs(elements))

    def calculate_std_with_built_in_function(self, matrix):
        """
        Calculate standard deviation using built-in np.std().

        Args:
            matrix: Input NumPy array

        Returns:
            float: Standard deviation rounded to 2 decimal places
        """
        elements = self._select_odd_negative_nums(matrix)
        return np.std(elements).round(2)

    def calculate_std_manually(self, matrix):
        """
        Calculate standard deviation manually using formula.

        Args:
            matrix: Input NumPy array

        Returns:
            float: Standard deviation rounded to 2 decimal places
        """
        elements = self._select_odd_negative_nums(matrix)
        amount_of_elements = len(elements)
        mean = np.sum(elements) / amount_of_elements
        deviation_squares = (elements-mean) ** 2
        return (np.sqrt(np.sum(deviation_squares) / amount_of_elements)).round(2)

    @staticmethod
    def _select_odd_negative_nums(matrix):
        """
        Select elements that are both odd and negative.

        Args:
            matrix: Input NumPy array

        Returns:
            np.ndarray: 1D array of negative odd numbers
        """
        elements = matrix[matrix % 2 == 1]
        return elements[elements < 0]
