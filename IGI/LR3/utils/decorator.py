'''
Module for time decorator.
'''
import time

def timer_decorator(func):
    """
    Decorator that measures and prints execution time of a function.

    Args:
        func: Function to be timed

    Returns:
        wrapper: Wrapped function with timing functionality

    Example:
        @timer_decorator
        def my_function():
            # function code
    """
    def wrapper(*args, **kwargs):
        """
        Wrapper function that adds timing before and after function call.

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            Result of the wrapped function
        """
        start = time.time()
        res = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"Elapsed time: {elapsed:.5f}")
        return res
    return wrapper