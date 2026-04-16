"""
Task 4. Module for abstract geometry figure.
"""
import abc

class GeometryFigure(abc.ABC):
    """
    Abstract base class for geometric figures.
    All specific figures must inherit from this class.
    """
    def __init__(self):
        """Initialize geometry figure."""
        pass

    @abc.abstractmethod
    def calculate_area(self):
        """
        Calculate and return area of the figure.

        Returns:
            float: Area of the figure
        """
        pass
