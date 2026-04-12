"""
Lab work 4. File work, classes, serializers, regular expressions, standard libraries.
Task 2. Text analysis using regular expressions.
Version 1.0
Developer: Morozova E.S.
Date: 12.04.2026
"""
from task2.file_operations_service import FileService

def run():
    """Execute task 2: analyze text, save results, create archive."""
    file_service = FileService()
    print("\nFILE SERVICE INFO:\n")
    print(file_service)
    print("\nSaving results to file...")
    file_service.save_info_to_file()
    print("\nResult archivation...")
    file_service.archive_file()
    print("\nArchived file info:")
    file_service.show_archived_info()
