"""
Task 5. Module for Array Creator.
"""
import numpy as np

class ArrayCreatorMixin:
    """Mixin providing array creation functionality."""
    @staticmethod
    def create_matrix(n: int, m: int):
        """
        Create a random integer matrix with values in range [-100, 100).

        Args:
            n: Number of rows
            m: Number of columns

        Returns:
            np.ndarray: Random integer matrix of shape (n, m)
        """
        return np.random.randint(-100, 100, (n, m))

    @staticmethod
    def matrix_creating_examples():
        """Demonstrate various NumPy array creation functions."""
        print(f"Zeros matrix:\n{np.zeros((2, 2))}")
        print(f"Ones matrix:\n{np.ones((2, 2))}")
        print(f"Diagonal matrix:\n{np.identity(2)}")
        print(f"Eye matrix:\n{np.eye(3, 3, k=1)}")
