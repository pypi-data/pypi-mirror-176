__all__ = ["infinite_number_a"]

import math


def infinite_number_a():
    k = 1.0
    sum = ((math.fabs(math.pow(math.cos(k), 2) - 0.51)*math.sin(3*k - 4) - 4.44 )*k)/k
    # Cycle for subtracting the number "e" from "sum".
    while True:
        k += k
        sum -= 0.001
        print("{:.3f}".format(sum))
