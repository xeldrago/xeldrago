def sayhello():
   print("HelloWorld")
while True:
       num = int(input("\njust say some number: "))
       if(num==0):
           number = "zero"
       elif(num%2==1):
           number = "odd"
       elif(num%2==0):
           number="even"
       else:
           number = "impossible. don't worry. you'll never get here."
   if(number[0] == 'e'):
       print("you have entered an even number")
   elif(number[0] == 'o'):
       print("you have entered an odd number")
   elif(number[0] == 'z'):
       print("you have entered zero. so let's just call it even.")
   else: 
       print("what kind of sorcery is this?")
