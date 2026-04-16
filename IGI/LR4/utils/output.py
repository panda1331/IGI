"""
This module implements console output functions.
"""

def console_menu():
    print("\nChoose an option:")
    print("0. Exit")

    print("1. Using serializer put data in file. Available options: reading, searching, sorting. \n   Formats CSV, module pickle")
    print("2. Text analyzer. Using regular expressions get info and export it in zipfile")
    print("3. Using task from Lab3 add new parameters ...")
    print("4. Geometric figures")
    print("5. NumPy")
    print("6. Pandas\n")

def task1_info():
    print("\nTask 1 info: Using serializer put data in file. Available options: reading,\nsearching, sorting. Formats CSV, module pickle\n")

def print_all_candidates_info(candidates: list) -> None:
    print("=" * 35)
    for candidate in candidates:
        print(candidate)
    print("=" * 35, "\n")

def print_passed_candidates_info(passed_candidates: list, amount_of_votes: int, pass_quote: float) -> None:
    print("2) Passed candidates: ")
    print(f"For passing candidate needs to get more than {amount_of_votes * pass_quote} votes")
    if len(passed_candidates) > 0:
        print_all_candidates_info(passed_candidates)
    else:
        print("No candidate to vote. Need to hold repeat elections\n")

def print_sorted_candidates_info(passed_candidates: list) -> None:
    print("3) Sorted (by amount of votes) candidates: ")
    sorted_candidates = sorted(passed_candidates)
    if len(passed_candidates) > 0:
        print_all_candidates_info(sorted_candidates)
    else:
        print("No candidate to vote. Need to hold repeat elections")

def task2_info():
    print("\nTask 2 info: ")

def task3_info():
    print("\nTask 3 info: ")

def print_table(x: float, n: int, f: float, mf: float, eps: float):
    """Print a table for task3."""
    print(f"{x} | {n} | {f} | {mf} | {eps}")

def task4_info() -> None:
    print("\nTask 4 info:")

def task5_info():
    print("\nTask 5 info: ")

def task6_info():
    print("\nTask 6 info: ")

