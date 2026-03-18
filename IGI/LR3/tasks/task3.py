"""
Task 3: Binary Number Validation.

Program checks if a user-entered string is a valid binary number.
A binary number can only contain digits 0 and 1.

Input: String from keyboard.
Output: Boolean result (True/False) indicating if string is binary.

Lab 3: Standard data types, collections, functions, modules.
Python 3.12.3.
Developer: Morozova E.S.
Date: 09.03.2026.
"""
from calculation.is_binary_num import is_binary
from utils.output import show_task3
from utils.input import input_str
def task3():
    """Execute task 3."""
    show_task3()
    user_input = input_str("Enter string: ").strip()
    print(f"String: {user_input} is binary num: {is_binary(user_input)}")