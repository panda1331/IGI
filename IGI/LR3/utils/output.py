"""
This module implements console output functions.
"""
def print_menu():
       """Print a menu."""
       print("\nChoose an option:\n"
           "1. Task 1.\n"
           "2. Task 2.\n"
           "3. Task 3.\n"
           "4. Task 4.\n"
           "5. Task 5.\n"
           "6. Exit the program.\n")

def show_task1():
    """Show info about task1."""
    print("\nTask 1. arcsin calculation using series expansion. Entering x, eps.\n")

def show_task2():
    """Show info about task2."""
    print("\nTask 2. Calculate sum of cubes in sequence. 12 - stop marker.\n")

def show_task3():
    """Show info about task3."""
    print("\nTask 3. Program analyses text and defines if the enterrd string is binary number.\n")

def show_task4():
    """Show info about task4."""
    print("\nTask 4. Find in text next options:\n"
          " a) determine amount of lowercase letters.\n"
          " b) find the last word containing the letter 'i' and its number.\n"
          " c) display the string excluding words starting with 'i'.\n")

def show_task5():
    """Show info about task5."""
    print("\nTask 5. Enter the sequence. \nProgram finds amount of elements that are bigger than C(input) and the product of the list elements up to the maximum absolute value element.\n")

def print_table(x:float, n:int, f: float, mf: float, eps:float):
       """Print a table for task1."""
       print(f"{x} | {n} | {f} | {mf} | {eps}")

def print_sum(summ: int):
       """Print a sum for task2."""
       print(f"Sum of cubes: {summ}\n")

def print_choice_task2():
    """Print a choice task2."""
    print("\nChoose an option:\n"
          "1. Generate sequence.\n"
          "2. Enter by yourself.\n")
