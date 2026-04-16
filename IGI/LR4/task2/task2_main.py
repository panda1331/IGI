"""
Lab work 4. File work, classes, serializers, regular expressions, standard libraries.
Task 2. Text analysis using regular expressions.
Version 1.0
Developer: Morozova E.S.
Date: 12.04.2026
"""
import re
from task2.file_operations_service import FileService

def run():
    """Execute task 2: analyze text, save results, create archive."""
    try:
        file_service = FileService()
        print("\nFILE SERVICE INFO:\n")
        print(file_service)
        print("\nSaving results to file...")
        file_service.save_info_to_file()
        print("\nResult archivation...")
        file_service.archive_file()
        print("\nArchived file info:")
        file_service.show_archived_info()
    except re.error as e:
        print(f"Regular expressions error: {e}")
    except FileNotFoundError as err:
        print(f"File not found: {err}")
    except PermissionError as err:
        print(f"Permission error: {err}")
    except IndexError as err:
        print(f"Index error: {err}")
    except Exception as e:
        print(f"Exception: {e}")
