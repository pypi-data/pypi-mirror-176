"""This is the squareFunc module which contains the
perfect_square() function which accepts
a number and prints the perfect squares of
all numbers from 1 up to the given number"""


def perfect_square():
    """Gets a number from user, prints out perfect squares
    up to that number"""
    myNum = eval(input("Enter any number: "))
    x = 1
    while(x<=myNum):
        print(f"{x} - {x**2}")
        x = x+1


perfect_square()