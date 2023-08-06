__all__ = ["math_fi_wi"]

import math

def math_fi_wi(x, a, b, c, d):
    # Calculation of Fi and Wi numbers
    fi = math.tan((x + a)) - math.log(11, math.fabs(b + 7))
    wi =c *((math.pow (x, 2)) + d * math.pow (math.e, 1.3)) ** (1./5.)
    
    def y():

        # Condition for comparison of functions
        # if |function| < 10; print (Res. Fi) 
        # if |function| >= 10; print (Res. Wi)

        if math.fabs(math.pow(math.sin(x), 2) * math.pow(math.cos(x), 3) - math.sin(x)+5.2)  < 10:
            print("Result fi:", fi)
        elif math.fabs(2* math.sin(x) * math.sin(2*x - 1.5) * math.cos(2 * x + 1.5)-6) >= 10:
            print("Result wi = {:.1f}".format(wi))
        else:
            print("None")
    y()
