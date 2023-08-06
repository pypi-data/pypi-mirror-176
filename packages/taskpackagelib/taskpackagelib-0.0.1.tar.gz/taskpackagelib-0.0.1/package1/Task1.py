
__all__ = ["grade"]


def grade(a, b, c):
    # A variety of wheat
    grade1 = [36, 40, 44]


    # The variety is divided by the size of the field
    sum1 = grade1[0] / a
    sum2 = grade1[1] / b
    sum3 = grade1[2] / c


    # Calculation of how much wheat was collected
    sum4 =(sum1 + sum2 + sum3)


    print("\n" + "Yield of the third grade:{:.2f}".format(sum1))
    print("Yield of the second grade:{:.2f}".format(sum2))
    print("Yield of the first grade:{:.2f}".format(sum3))
    print("A total of three fields:{:.2f}".format(sum4))
    int()
