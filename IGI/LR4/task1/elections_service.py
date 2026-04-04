from task1.candidate import Candidate
from task1.csv_parser import CsvParser
from task1.pickle_parser import PickleParser
from task1.seed_service import SeedService
from utils.output import print_all_candidates_info, print_passed_candidates_info, print_sorted_candidates_info


class ElectionsService:
    """
    Main service for election management.
    Handles voting, candidate serialization, and candidate search.
    """

    AMOUNT_OF_VOTERS = 2000
    PASS_QUOTE = 0.333

    def __init__(self):
        """Initialize empty candidates list and load initial data."""
        self.candidates = []
        self.initialize_candidates()

    def initialize_candidates(self):
        """Load hardcoded candidate data from SeedService and create Candidate objects."""
        initialize_service = SeedService()
        candidates_dict = initialize_service.initialize_candidates()
        self.candidates = [Candidate(name, votes) for name, votes in candidates_dict.items()]

    @property
    def get_candidates(self) -> list:
        """Return list of all candidates."""
        return self.candidates


    def voting(self) -> None:
        """
        Main voting process:
        1. Serialize candidates to CSV and pickle
        2. Deserialize from pickle
        3. Display all candidates
        4. Determine who passed (votes > 2000 * 0.333)
        5. Display passed candidates and sorted results
        """
        # initialize_service = SeedService()
        csv_parser = CsvParser("task1/candidates.csv")
        pickle_parser = PickleParser("task1/candidates.pickle")

        # candidates_dict = initialize_service.initialize_candidates()
        candidate_object_list = self.get_candidates

        csv_parser.serialize(candidate_object_list)
        pickle_parser.serialize(candidate_object_list)

        candidates_from_pickle = pickle_parser.deserialize()
        print("1) All candidates:")
        print_all_candidates_info(candidates_from_pickle)

        passed_candidates = []

        for c in candidates_from_pickle:
            if c.number_of_votes > ElectionsService.AMOUNT_OF_VOTERS * ElectionsService.PASS_QUOTE:
                passed_candidates.append(c)

        print_passed_candidates_info(passed_candidates, ElectionsService.AMOUNT_OF_VOTERS, ElectionsService.PASS_QUOTE)
        print_sorted_candidates_info(candidates_from_pickle)

    def search_candidate(self, name: str):
        """
        Search for a candidate by name (case-insensitive).

        Args:
            name: Candidate name to search for

        Prints candidate info if found, otherwise "No such candidate".
        """
        for candidate in self.candidates:
            if candidate.name.lower() == name.lower():
                print(candidate)
                return
        print("No such candidate")
        return



