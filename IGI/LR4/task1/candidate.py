"""
Task 1. Module provides class Candidate.
"""
class Candidate:
    """Candidate with name and votes. Supports comparison by votes."""
    def __init__(self, name: str, number_of_votes: int) -> None:
        """Initialize candidate."""
        self.__name = name
        self.__number_of_votes = number_of_votes

    def __str__(self) -> str:
        """Return 'Candidate: {name}, {votes} votes'."""
        return f"Candidate: {self.__name}, {self.__number_of_votes} votes"

    def __gt__(self, other) -> bool:
        """Compare by votes (greater than)."""
        return self.__number_of_votes > other.get_number_of_votes()

    def __lt__(self, other) -> bool:
        """Compare by votes (less than)."""
        return self.__number_of_votes < other.get_number_of_votes()

    def get_name(self) -> str:
        """Return candidate name."""
        return self.__name

    def get_number_of_votes(self) -> int:
        """Return vote count."""
        return self.__number_of_votes

    def set_number_of_votes(self, number_of_votes: int) -> None:
        """Set vote count."""
        if 0 <= number_of_votes <= 2000:
            self.__number_of_votes = number_of_votes
