"""
Lab work 4. File work, classes, serializers, regular expressions, standard libraries.
Task 1. Election vote analysis.
Version 1.0
Developer: Morozova E.S.
Date: 12.04.2026
"""
import csv
import pickle

from task1.elections_service import ElectionsService
from utils.input import input_str
from utils.output import task1_info

def run() -> None:
    """Execute task1. """
    task1_info()
    try:
        elections = ElectionsService()
        elections.voting()
        elections.sorted_candidates()
        print("4) Searching for candidate")
        name = input_str("Enter name: ")
        elections.search_candidate(name)
    except csv.Error as err:
        print(f"Parsing csv error: {err}")
    except FileNotFoundError as err:
        print(f"File not found: {err}")
    except PermissionError as err:
        print(f"Permission error: {err}")
    except pickle.PicklingError as err:
        print(f"Serialization pickle error: {err}")
    except pickle.UnpicklingError as err:
        print(f"Deserialization pickle error: {err}")
    except Exception as e:
        print(f"Exception: {e}")

