try:
   a=0
   while a!=1000:
    num1 = float(input("enter first number: "))
    num2 = float(input("enter second number: "))
    op = input("enter the operator: ")
    if op == "+":
      print(num1+num2)
    elif op == "-":
      print(num1-num2)
    elif op == "*":
      print(num1*num2)
    elif op == "/":
      print(num1/num2)
    a=+1
except:
    print("invalid input boy")
    
