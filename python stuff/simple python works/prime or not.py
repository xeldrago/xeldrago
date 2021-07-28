i=0
while (i!=13): 
    print(16*i)
    i+=1
num=int(input("enter the number ,u wana check prime or not"))
for x in range(2,num):
	if num%x==0:
		print(num,"is not a prime ")
		break
else:
	print(num,"is a prime")		    
