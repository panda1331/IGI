"""
Task 1. Module for CSV parsing.
"""
import csv

from task1.candidate import Candidate
from task1.parser_base import ParserBase

class CsvParser(ParserBase):
    """CSV serializer/deserializer for Candidate objects."""
    def __init__(self, filename: str):
        """Set path to CSV file."""
        self.file_name = filename

    def serialize(self, candidates: list):
        """Save list of Candidate objects to CSV file."""
        candidates_dicts_list = []
        for candidate in candidates:
            candidates_dicts_list.append({"name": candidate.get_name(), "number_of_votes": candidate.get_number_of_votes()})

        with open(self.file_name, 'w', newline='') as csvfile:
            columns = ['name', 'number_of_votes']
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            writer.writerows(candidates_dicts_list)

    def deserialize(self):
        """Load list of Candidate objects from CSV file."""
        with open(self.file_name, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            candidates = []
            for row in reader:
                candidates.append(Candidate(row['name'], int(row['number_of_votes'])))
        return candidates