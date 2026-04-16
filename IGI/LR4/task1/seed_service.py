"""
Task 1. Module for SeedService.
"""
class SeedService:
    @staticmethod
    def initialize() -> dict:
        """Initialize SeedService."""
        candidates = {"Ivanov": 850, "Petrov": 620, "Sidorov": 430, "Kozlov": 720, "Smirnov": 380}
        return candidates