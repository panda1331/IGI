"""
Lab 3.  Standard data types, collections, functions, modules.  Python 3.12.3.  Morozova E.S.  09.03.2026.
"""

from tasks.task1 import *
from tasks.task2 import *
from tasks.task3 import *
from tasks.task4 import *
from tasks.task5 import *
from utils.output import *
from utils.input import *

def main():
    """Execute the program."""
    while(True):
        print_menu()
        choice = input_int(1, 6, "Enter your choice: ")
        match choice:
            case 1:
                task1()
            case 2:
                task2()
            case 3:
                task3()
            case 4:
                task4()
            case 5:
                task5()
            case 6:
                break

if __name__ == "__main__":
    main()


