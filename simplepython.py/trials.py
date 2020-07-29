

dict={1:2,2:3}
users={}

for k,v in dict.items():
   k=input("username")
   v=dict.get(k)
   v=input("password")
   print(k,v)
   users.update([(k,v)])
   print(users)
print(users)
if 

