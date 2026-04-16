"""
Lab work 4. File work, classes, serializers, regular expressions, standard libraries.
Task 6. CSV-file statistical analysis.
Version 1.0
Developer: Morozova E.S.
Date: 12.04.2026
"""
from task6.lib_service import LibService
from utils.output import task6_info
import pandas as pd


def run():
    """Execute task 6: weather dataset analysis."""
    try:
        task6_info()
        lib_service = LibService()
        print("Task A. Pandas Library. Structures Series and DataFrame\n")
        lib_service.select_first_records(7)
        print("\nTask B. Basic operations and statistical analysis\n")
        lib_service.statistical_analysis()
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except PermissionError as e:
        print(f"Permission error: {e}")
    except pd.errors.EmptyDataError as e:
        print(f"Empty data file: {e}")
    except pd.errors.ParserError as e:
        print(f"Parser error: {e}")
