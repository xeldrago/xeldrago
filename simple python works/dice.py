import random
i=1000
while i!=0:
  i-=1  
  dice1=[1,2,3,4,5,6]
  dice2=[1,2,3,4,5,6]
  se=input("to dice roatate say, 'yes':")
  if se == 'yes':
   die1=random.choices(dice1)
   die2=random.choices(dice2)
   print("The values are....",die1,die2)
  else:
   print("have a nice day")
