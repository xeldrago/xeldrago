def food(f):
    f+=f*0.1
    return f/num
def movie(m):
    m+=m*0.1
    
    return m/num
num=int(input("how many are there"))
ftotal=int(input("amount for food"))
mtotal=int(input("amound for movie"))
x=food(ftotal)
y=movie(mtotal)
print(x+y)
