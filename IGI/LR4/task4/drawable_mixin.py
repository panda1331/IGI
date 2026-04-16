"""
Task 4. Draw parallelogram.
"""
import math
import matplotlib.pyplot as plt
import numpy as np

class DrawableMixin:
    """Mixin providing drawing functionality for parallelogram."""
    def draw(self, caption: str):
        """
        Draw parallelogram using matplotlib.

        Builds vertices from diagonals and angle, then plots and fills the shape.

        Args:
            caption: Text label displayed at the center of the parallelogram.
        """
        angle = self.angle
        half_d1 = self.diagonal1 / 2
        half_d2 = self.diagonal2 / 2

        x_array = [-half_d1, half_d2 * math.cos(angle), half_d1, -half_d2 * math.cos(angle), -half_d1]
        y_array = [0, half_d2 * math.sin(angle), 0, -half_d2 * math.sin(angle), 0]
        x = np.array(x_array)
        y = np.array(y_array)

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.grid(True, zorder=0)

        textcolor = "black"
        if self.color == "black" or self.color == "blue":
            textcolor = "white"
        ax.text(0, 0, caption, color=textcolor, fontsize=16, ha="center", va="center")

        ax.plot(x, y, self.color, zorder=2, label="Parallelogram")
        ax.fill(x, y, self.color, zorder=2)
        ax.axis('equal')

        ax.set_xlabel("x", fontsize=20)
        ax.set_ylabel("y", fontsize=20)
        ax.legend(fontsize=16)

        plt.savefig("task4/parallelogram.png")
        plt.show()
