def food(f):
    f+=f*0.1
    #return f/num
def movie(m):
    m+=m*0.1
    
    #return m/num
num=int(input("h"))
ftotal=int(input("j"))
mtotal=int(input("t"))
x=food(ftotal)
y=movie(mtotal)
print(x+y)
