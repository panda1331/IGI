"""
Lab work 4. File work, classes, serializers, regular expressions, standard libraries.
Version 1.0
Developer: Morozova E.S.
Date: 12.04.2026
"""
from task1 import task1_main
from task2 import task2_main
from task3 import task3_main
from task4 import task4_main
from task5 import task5_main
from task6 import task6_main
from utils.input import input_int
from utils.output import console_menu

def main():
    while True:
        console_menu()
        choice = input_int(0, 6, "Input num of task: ")
        match choice:
            case 0:
                break
            case 1:
                task1_main.run()
            case 2:
                task2_main.run()
            case 3:
                task3_main.run()
            case 4:
                task4_main.run()
            case 5:
                task5_main.run()
            case 6:
                task6_main.run()

if __name__ == "__main__":
    main()