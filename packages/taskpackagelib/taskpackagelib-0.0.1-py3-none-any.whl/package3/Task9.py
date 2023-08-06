__all__ = ["company_calculations"]

import math
from array import array

def company_calculations():
    # Years.
    k = [1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001]
    sum = 0
    y = 0
    f = 0
    # A cycle for calculating the company's losses and profits.
    for i in range(0, 11):

        y = ((math.fabs(math.cos((math.pow(k[i], 2) - 3.8))))/ 4.5 - 9.7 * math.sin(k[i]-3.1))
        f += y

        if y == sum:
            print("This year, the company had no profits and losses:{:.0f}".format (k[i]), "," "   The company made money = {:.1f}".format (y) )

        if y > sum:
            print("In this year, the company had:{:.0f}".format (k[i]), "," "   The company made money = {:.1f}".format (y) )

        if y < sum:
            print("This year the company had losses: {:.0f}".format (k[i]), "," "   The company made money = {:.1f}".format (y) )



    # Comparison condition
    if y >= 230 and y <= 8500: 
        print("In total, the company earned: {:.0f}".format(f))
        print(len(k) -1 , ":years the company had profits")
    else:
        print("There were no incomes in the range from 230 to 8500!")
            









