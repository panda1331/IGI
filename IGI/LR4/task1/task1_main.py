from task1.elections_service import ElectionsService
from utils.input import input_str
from utils.output import task1_info

def run() -> None:
    task1_info()

    elections = ElectionsService()
    elections.voting()
    print("4) Searching for candidate")
    name = input_str("Enter name: ")
    elections.search_candidate(name)
    return

