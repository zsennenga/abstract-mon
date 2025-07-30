import math


def bound_positive_int(value: int | float) -> int:
    return max(math.floor(value), 0)
