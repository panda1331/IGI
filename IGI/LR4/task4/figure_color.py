"""
Task 4. Module for figure color.
"""
class FigureColor:
    """Class to store color of a geometric figure."""
    def __init__(self, color):
        """
        Initialize figure color.

        Args:
            color: Name of the color (e.g., 'red', 'blue', 'green')
        """
        self.__color = color

    @property
    def color(self):
        """
        Get color of the figure.
        Returns:
            str: Color name
        """
        return self.__color

    @color.setter
    def color(self, value):
        """
        Set color of the figure.
        Args:
            value: New color name
        """
        self.__color = value

