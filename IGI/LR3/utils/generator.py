'''
Module for generator function and initialization.
'''

import random
from typing import Any, Generator


def num_generator_float(n: int):
    """Generator for integer numbers with number 12 required."""
    twelve_pos = random.randint(0, n-1)
    for i in range(n):
        if i == twelve_pos:
            break
        else:
            yield random.uniform(-1000, 1000)

def generate_sequence_float(seq: list, n: int) -> list:
    """Generate sequence using generator."""
    for number in num_generator_float(n):
        seq.append(number)
    return seq