"""
Task 3. Series Calculation Service.
"""
import statistics
from math import asin, fabs
from utils.output import print_table


class SeriesCalculationService:
    """Service for calculating arcsin series and its statistics."""
    def __init__(self, x: float, eps: float):
        """
        Initialize series calculator.
        Args:
            :param x: Value in range (-1, 1) for arcsin calculation
            :param eps: Precision threshold for series convergence
        """
        self.__x = x
        self.__eps = eps
        self.__series_values = self.calculate_series()

    def __str__(self) -> str:
        """Return formatted statistics report."""
        return str(f"1) Mean: {self.calculate_mean()}\n"
                   f"2) Mode: {self.calculate_mode()}\n"
                   f"3) Median: {self.calculate_median()}\n"
                   f"4) Variance: {self.calculate_variance()}\n"
                   f"5) Standard deviation: {self.calculate_standard_deviation()}")

    def get_series_values(self) -> tuple[float, list[int], list[float], list[float], int, float]:
        """
        Return complete series calculation result.

        Returns:
            tuple: (x, iterations, series_values, arcsin_values, break_iteration, break_value)
        """
        return self.__series_values

    @property
    def series_list(self) -> list[float]:
        """Return list of partial series sums."""
        return self.__series_values[2]

    def calculate_series(self) -> tuple[float, list[int], list[float], list[float], int, float]:
        """
        Compute arcsin series expansion.

        Returns:
            tuple: (x, iterations, series_values, arcsin_values, break_iteration, break_value)
        """
        series = self.__x
        a = self.__x

        break_iteration = -1
        break_value = -1
        iterations = []
        series_values = []
        arcsin_values = []
        arcsin_value = asin(self.__x)
        for i in range(500):
            print_table(self.__x, i, series, arcsin_value, self.__eps)
            a *= (2*i + 1) ** 2 * self.__x ** 2 / ((2*i + 2)*(2*i + 3))
            series += a

            iterations.append(i)
            series_values.append(series)
            arcsin_values.append(arcsin_value)

            if fabs(arcsin_value - series) < self.__eps:
                break_iteration = i
                break_value = series
                break

        return self.__x, iterations, series_values, arcsin_values, break_iteration, break_value

    def calculate_mean(self) -> float:
        """Return mean of series values."""
        return statistics.mean(self.series_list)

    def calculate_mode(self) -> float:
        """Return mode of series values."""
        return statistics.mode(self.series_list)

    def calculate_median(self) -> float:
        """Return median of series values."""
        return statistics.median(self.series_list)

    def calculate_variance(self) -> float:
        """Return variance of series values."""
        return statistics.pvariance(self.series_list)

    def calculate_standard_deviation(self) -> float:
        """Return standard deviation of series values."""
        return statistics.pstdev(self.series_list)
