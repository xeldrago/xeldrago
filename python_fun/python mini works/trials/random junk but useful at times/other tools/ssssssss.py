def n(x) :
    a,b=0,1
    c=0
    while a<=x:
        print(a,end=',')
        c+=1
        print(c)
        a,b=b,a+b
x=int(input("x;"))
n(x)
