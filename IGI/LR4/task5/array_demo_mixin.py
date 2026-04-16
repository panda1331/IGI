"""
Task 5. Module for Array Demonstration Mixin.
"""
import numpy as np

class ArrayDemoMixin:
    """Mixin providing NumPy array demonstration functionality."""
    @staticmethod
    def matrix_indexing_slicing_example(matrix):
        """
        Demonstrate array indexing and slicing.

        Args:
            matrix: 2D NumPy array to demonstrate on
        """
        print(f"Matrix first element: {matrix[0][0]}")
        print(f"Matrix [1..n-1][1..m-1] elements (inside square): \n{matrix[1:len(matrix) - 1, 1: len(matrix[0]) - 1]}")
        print(f"Index od max element: {matrix.argmax()}")
        print(f"Index od min element: {matrix.argmin()}")

    @staticmethod
    def matrix_operations_example():
        """
        Demonstrate universal (element-wise) operations on arrays.
        Shows addition, multiplication, subtraction, division, modulo,
        power and square root.
        """
        a = np.array([[1, 2, 3], [4, 5, 6]], float)
        b = np.array([[10, 11, 12], [13, 14, 15]], float)
        print(f"\nMatrix a:\n{a}")
        print(f"\nMatrix b:\n{b}")
        print(f"\n1) a + b\n{a + b}")
        print(f"\n2) a * b\n{a * b}")
        print(f"\n3) a - b\n{a - b}")
        print(f"\n4) a / b\n{a / b}")
        print(f"\n5) b % a\n{b % a}")
        print(f"\n6) a ** b\n{a ** b}")
        print(f"\n7) sqrt(a)\n{np.sqrt(a)}")

    @staticmethod
    def statistics_info(matrix):
        """
        Calculate and return basic statistics for the matrix.

        Args:
            matrix: 2D NumPy array

        Returns:
            str: Formatted string with mean, median, correlation,
                 variance and standard deviation
        """
        return (f"\n--- Statistics info: ---\n"
                f"  Mean: {np.mean(matrix)}\n"
                f"  Median: {np.median(matrix)}\n"
                f"  Corrective coefficients: \n{np.corrcoef(matrix)}\n"
                f"  Variance: {np.var(matrix)}\n"
                f"  Standard deviation: {np.std(matrix)}\n")
