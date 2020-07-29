
def checkmoney(t):
    print(t)
    if t < 7000:
        print( "Ahem, can you rethink this number please?")
    elif t >= 10000:
        print("Wow sis! You are a queen")
    elif t in range(7000,10001):
        print("Cool, thanks sis! x rupees will certainly help.")

    return
i=0
while i!=12:
 sis=int(input("Yeah…yeah…how much?"))
 checkmoney(sis)
