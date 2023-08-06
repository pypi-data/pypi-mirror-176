__all__ = ["product_sum"]

import math

def product_sum(k):
    z = 0
    x = 0
    y = 1
    # Cycle for calculating the amount
    for i in range(5):
        if i <= 16:
            x += 13.4 * math.sin(-1.26)* math.cos(math.fabs(k/7.5))  # funtion for sum
        print("Sum = {:.1f}".format (x))
    # Cycle for calculating the product
    for i in range(5):
        if i <= 16:
            y *= 2 * math.sin(math.fabs( 2* k)) * math.cos(2 * k) - 11.6 * math.sin(k/0.4-1)  # funtion for product
        print("Product = {:.1f}".format (y))

    z = math.tan(x + y) # addition with tan 
    print("z = {:.1f}".format (z))  
