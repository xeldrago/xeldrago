C=[]
T=[]
def g():
  A=input('login id:')
  B=input('password:')
  
  if A and B in C:
   print('ur in')
   print('hafun')
   exit()
  else:
   print('no u havent signed up so ,sign up')
   D=input('new login')
   F=input('new password')
   C.insert(len(C),D)
   C.insert(len(C),F)
   print('now u hv an account to log in')
   
   
       
i=input('welcome bish, press y to get to it or q to quit and die')
while i!='q':
    g()
  
print('as u wish die') 
