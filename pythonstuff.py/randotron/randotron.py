from random import randint
def p():
 while True:
   lower=int(input("enter the lower limit"))
   upper=int(input("enter upper limit"))
   amount=int(input("enter the number of numbers to be picked at random"))
   a=int(randint(lower,upper))
   
   for i in range(0,amount):
     #print(a)
     gues=[]
     while a not in gues:
       gues.insert(len(gues),int(input('guess the number in between 1 to 10 ,have {} chances!'.format(upper))))
       if a in gues:
        print("aha nice!")
       else:
         
         print("keep it coming,try try..")  
           
    
 print(randint(lower, upper),end=" ")
 print("\n")
p()            


          
