__all__ = ["tabulation_x_y"]

import math

def tabulation_x_y(k, cycle):
    sum_y = 0
    y = 0
    f = math.fabs(math.sin(12*k) * math.cos(math.fabs(2*k) )/3) + 4.21
    x = 0
    h = 0
    for i in range(cycle):
        if x <= cycle:
            h += 1.1
            y += f
        print("x = {:.1f}".format(h) ,", " "y = {:.1f}".format(y))
    
    sum_y = math.fabs(y - f)
    print("y = {:.1f}".format(sum_y))
