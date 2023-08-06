__all__ = ["infinite_number_b"]

import math

def infinite_number_b():

    sum = 0.0
    e = 0.001
    x = 1.0
    k = 1.0
    factorial = k * k
    sum = (math.pow(-1, k) * ((math.fabs(math.pow(math.cos(k), 2) - 0.51)*math.sin(3*k - 4) - 4.44) * math.pow(x, 1)* factorial)) 

    while True:
        k  += k
        if sum > e:
            sum -= e
        else:
            break
        print("{:.3f}".format(sum))




















# infinite_number_b()















    # if sum > e:
    #     print("{:.3f}".format(sum -= 1))
    # if sum < e:
    #     print("{:.3f}".format(sum + 1))
    # if sum == e:





    #     k = 1
    #     k += k
    #     if sum > e:
    #         print(sum)
    #         sum - 1
    #     if sum == e:
    #         print(sum)
    #     else:
    #         print(sum)
    #         sum + 1
    #     print("{:.3f}".format(sum))
    # print("{:.3f}".format(sum))
    # int()