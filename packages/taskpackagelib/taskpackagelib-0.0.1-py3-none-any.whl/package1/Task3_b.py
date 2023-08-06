
__all__ = ["tax_salary"]

import math


def tax_salary(x):
    # Salary calculation
    salary1 = 100 * math.fabs(math.pow(math.sin(x), 2)* math.pow(math.cos(x), 3) - math.sin(x)+5.2 * (11) + 50)         #
    salary2 = 150 * math.fabs(2* math.sin(x) * math.sin(2*x - 1.5) * math.cos(2 * x + 1.5)-6 * (11) + 100)              # Salary calculation
    salary3 = 200 * math.fabs( math.fabs(math.pow(math.cos(x), 2) - 0.51) * math.sin(3*x - 4) - 4.44 * (11) + 135)      #
    # Tax calculation
    tax1 = (salary1 / 100) * 10
    tax2 = (salary2 / 100) * 10 
    tax3 = (salary3 / 100) * 10

    print("The tax on the amount of wages for type A work is 10%= {:.1f}".format (tax1))
    print("The tax on the amount of wages for type B work is= {:.1f}".format (tax2))
    print("The tax on the amount of wages for type C work is= {:.1f} \n".format (tax3))

    print("The total amount of wages for type A work is={:.1f}".format (salary1 - tax1))
    print("The total amount of wages for type B work is={:.1f}".format (salary2 - tax2))
    print("The total amount of wages for type C work is={:.1f}".format (salary3 - tax3))
