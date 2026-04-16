"""
Task 1. Module for ParserBase.
"""
import abc

class ParserBase(abc.ABC):
    """Abstract base class for serialization/deserialization."""
    @abc.abstractmethod
    def serialize(self, candidates: list):
        """Save candidates list to storage."""
        pass
    @abc.abstractmethod
    def deserialize(self):
        """Load candidates list from storage and return it."""
        pass
