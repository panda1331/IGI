"""
Task 1. Module for PickleParser.
"""
import pickle

from task1.parser_base import ParserBase


class PickleParser(ParserBase):
    
    def __init__(self, file_name):
        """Initialize PickleParser."""
        self.file_name = file_name

    def serialize(self, candidates: list):
        """Serialize PickleParser."""
        with open(self.file_name, "wb") as f:
            pickle.dump(candidates, f)

    def deserialize(self):
        """Deserialize PickleParser."""
        candidates = []
        with open(self.file_name, "rb") as f:
            candidates = pickle.load(f)

        return candidates

