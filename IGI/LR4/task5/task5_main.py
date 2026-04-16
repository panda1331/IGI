"""
Lab work 4. File work, classes, serializers, regular expressions, standard libraries.
Task 5. Matrix operations with NumPy.
Version 1.0
Developer: Morozova E.S.
Date: 12.04.2026
"""
from task5.array_service import ArrayService
from utils.input import input_int
from utils.output import task5_info


def run():
    """Execute task 5. """
    try:
        task5_info()
        n = input_int(1, 100, "Enter n rows: ")
        m = input_int(1, 100, "Enter m columns: ")
        array_service = ArrayService()
        a = array_service.create_matrix(n, m)
        print(f"Created matrix: \n{a}")

        print("\n--- Matrix creating examples: ---")
        array_service.matrix_creating_examples()
        print("\n--- Matrix indexing and slicing examples: ---")
        array_service.matrix_indexing_slicing_example(a)
        print("\n--- Matrix operations examples: ---")
        array_service.matrix_operations_example()

        print(array_service.statistics_info(a))

        print(f"\nMatrix summary of modules of negative numbers: {array_service.calculate_sum_of_abs_negative_numbers(a)}")
        print(f"Built-in calculated square deviation: {array_service.calculate_std_with_built_in_function(a)}")
        print(f"Manually calculated square deviation: {array_service.calculate_std_manually(a)}")
    except ZeroDivisionError as e:
        print(f"ZeroDivisionError: {e}")
    except ValueError as e:
        print(f"ValueError: {e}")