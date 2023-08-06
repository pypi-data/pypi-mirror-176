__all__ = ["complex_search"]

from array import array
import math


def complex_search():
    k = 1
    i = 1
    a = []
    # Cycle for add function (b) to list (a)
    for i in range(0, 7):
        y = round ((13.4 * math.sin(-1.26)* math.cos(k)* math.fabs(k/7.5))* k)
        k+=1
        a.append(y)
    # Change the penultimate number in the list
    for i in range(0, 7):
        a[-2] = a[-4]
        print("{:.2f}".format(a[i]))
    


