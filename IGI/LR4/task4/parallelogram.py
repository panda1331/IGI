"""
Task 4. Module for parallelogram.
"""
import math
from task4.drawable_mixin import DrawableMixin
from task4.figure_color import FigureColor
from task4.geometry_figure import GeometryFigure

class Parallelogram(GeometryFigure, DrawableMixin):
    """Parallelogram defined by two diagonals and angle between them."""

    name = "Parallelogram"
    def __init__(self, diagonal1,diagonal2, angle, color):
        """
        Initialize parallelogram.

        Args:
            diagonal1: Length of first diagonal
            diagonal2: Length of second diagonal
            angle: Angle between diagonals in degrees
            color: Color name for the figure
        """
        super().__init__()
        self.__diagonal1 = diagonal1
        self.__diagonal2 = diagonal2
        self.__angle = angle
        self.__color = FigureColor(color)

    @classmethod
    def get_name(cls):
        """Return figure name (class method)."""
        return f"\nFigure name: {cls.name}"

    @property
    def diagonal1(self):
        """Get first diagonal length."""
        return self.__diagonal1

    @property
    def diagonal2(self):
        """Get second diagonal length."""
        return self.__diagonal2

    @property
    def angle(self):
        """Get angle in radians (converted from degrees)."""
        return math.radians(self.__angle)

    @property
    def color(self):
        """Get figure color."""
        return self.__color.color

    def calculate_area(self):
        """
        Calculate area using formula: 0.5 * d1 * d2 * sin(angle).

        Returns:
            float: Area of the parallelogram
        """
        return 0.5 * self.__diagonal1 * self.__diagonal2 * math.sin(self.angle)

    def get_info(self):
        """
        Return formatted string with figure parameters, color and area.

        Returns:
            str: Formatted info string
        """
        return "Diagonal 1: {}\nDiagonal 2: {}\nAngle: {}° \nArea: {:.4f}\nColor: {}".format(self.__diagonal1, self.__diagonal2, self.__angle, self.calculate_area(), self.__color.color)
