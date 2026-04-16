"""
Lab work 4. File work, classes, serializers, regular expressions, standard libraries.
Task 3. Series calculation with graphics.
Version 1.0
Developer: Morozova E.S.
Date: 12.04.2026
"""
from statistics import StatisticsError

from task3.series_calculation_service import SeriesCalculationService
from task3.visualisation_service import VisualisationService
from utils.input import input_float
from utils.output import task3_info

def run():
    """Execute task3."""
    try:
        task3_info()
        x = input_float(-1.0, 1.0, "Enter x: ")
        eps = input_float(0.0, 1.0, "Enter eps: ")
        calculation_service = SeriesCalculationService(x, eps)
        visualisation_service = VisualisationService()
        print(calculation_service)
        visualisation_service.draw(calculation_service.get_series_values())
    except StatisticsError as e:
        print(f"Statistics exception: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except PermissionError as e:
        print(f"Permission error: {e}")
    except Exception as e:
        print(f"Exception: {e}")

