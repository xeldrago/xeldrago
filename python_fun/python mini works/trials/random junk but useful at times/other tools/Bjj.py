import sys

def Factorial(n): # Return factorial
    result = 1
    for i in range (1,n):
        result = result * i
    print ("factorial is ",result)
    return result
