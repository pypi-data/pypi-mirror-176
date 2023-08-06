
__all__ = ["choice_month_if"]


def choice_month_if(i):
    x = ["The first quarter", "Second quarter", "The third quarter", "The fourth quarter"]
    # Condition of quarters
    if i == 1 or i == 2 or i == 3:  #
        print(x[0])
    elif i == 4 or i == 5 or i == 6:
        print(x[1])
    elif i == 7 or i == 8 or i == 9:
        print(x[2])
    elif i == 10 or i == 11 or i == 12:
        print(x[3])
    else:
        print("No more months)")

