def fibonacci(n):  
   if n <= 1:  
       return n  
   else:  
       return(fibonacci(n-1) + fibonacci(n-2))  

nterm = int(input("number of terms u want= "))  
 
if nterm <= 0:  
   print("invalid bruv,enter a positive number maybe")  
else:  
   print("Fibonacci sequence tada:")  
   for i in range(nterm):  
       print(fibonacci(i))  
