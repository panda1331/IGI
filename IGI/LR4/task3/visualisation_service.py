import matplotlib
import matplotlib.pyplot as plt
import numpy as np

class VisualisationService:
    @staticmethod
    def _draw_plot(n, y_series, y_math, x_value):
        """
        Create base plot with axes, grid, labels and legend.
        Args:
            n: Array of iteration numbers (x-axis)
            y_series: Array of series partial sums
            y_math: Array of math.asin() reference values
            x_value: Original x parameter for title

        Returns:
            tuple: (fig, ax) matplotlib figure and axes objects
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.plot(n, y_series, 'blue', label="Series")
        ax.plot(n, y_math, 'red', label="Math")

        ax.grid(True)
        ax.set_xlabel("n", fontsize=20)
        ax.set_ylabel("y", fontsize=20)
        ax.set_title(f"Convergence of the series to arcsin({x_value})", fontsize=20)
        ax.text(0.6, 0.4, "Series convergence graph", transform=ax.transAxes, fontsize=12, ha='left', va='top')
        ax.legend(fontsize=16)

        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        return fig, ax

    @staticmethod
    def _add_annotation(ax, break_iteration, break_value):
        """
        Add annotation to axes object.
        Args:
            ax: Matplotlib axes object
            break_iteration: Iteration number where precision was reached
            break_value: Series value at that iteration
        """
        x_text = float(break_iteration - break_iteration*0.01)
        y_text = float(break_value - break_value*0.01)
        ax.annotate('Convergence', xy=(break_iteration, break_value), xytext=(x_text, y_text),
                    arrowprops=dict(arrowstyle='->'), fontsize=16)

    def draw(self, series_result: tuple[float, list[int], list[float], list[float], int, float]):
        """
        Main method to plot and save the convergence graph.

        Args:
            series_result: Tuple containing (x, iterations, series_values,
                          arcsin_values, break_iteration, break_value)
        """
        x_value = series_result[0]
        n = np.array(series_result[1], float)
        y_series = np.array(series_result[2], float)
        y_math = np.array(series_result[3], float)
        break_iteration = series_result[4]
        break_value = series_result[5]

        fig, ax = self._draw_plot(n, y_series, y_math, x_value)
        self._add_annotation(ax, break_iteration, break_value)

        plt.savefig("task3/convergence.png")
        plt.show()
