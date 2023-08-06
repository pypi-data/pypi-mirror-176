
__all__ = ["triangle"]

import math

def triangle(a, b, c):

    # Calculations of the sides of a triangle
    side1 = math.sqrt((math.pow(a[0] - a[1], 2)) + (math.pow(b[0] - b[1], 2)))
    side2 = math.sqrt((math.pow(b[0] - b[1], 2)) + (math.pow(c[0] - c[1], 2)))
    side3 = math.sqrt((math.pow(c[0] - c[1], 2)) + (math.pow(a[0] - a[1], 2)))

    #Semiperimeter
    p = (side1+side2+side3)/3

    # Height
    h = (2 / side1) * math.sqrt (p * (p - side1) * (p - side2) * (p - side3))

    # Median
    l = math.sqrt(side1 * side2 * (side1 + side2 + side3) * (side1 + side2 - side3)) / side1 + side2

    print("Height h = {:.1f}".format(h))
    print("Median W = {:.1f}".format(l))
