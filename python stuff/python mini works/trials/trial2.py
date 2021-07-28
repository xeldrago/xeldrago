print('hi this aint "nice"')
print('you'+'me')
def home_view():
    f=open("index.html",'r')
    return f.read()
    f.close()

home_view()