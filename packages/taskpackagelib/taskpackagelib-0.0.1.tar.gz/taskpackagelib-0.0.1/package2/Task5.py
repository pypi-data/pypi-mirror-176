__all__ = ["table_of_measures"]

import math

# Units of information
def table_of_measures(sum1, sum2, n):
    
    for i in range(n):
        print("Cheldron = {:.3f}".format (sum2), "Л = {:.3f}".format (sum1), "Peka")
        # Every cycle the number is added to the old number.
        sum1 += 0.149
        sum2 += 1.309
        print("Cheldron = {:.3f}".format (sum2), "Л = {:.3f}".format (sum1), "Peka") 

