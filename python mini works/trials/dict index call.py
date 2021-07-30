from collections import OrderedDict
#but since python is awesome and now in 3.9 i think lol 
dict={0:{10:'some value'}, 1:{12:'some other value'}}
dictlist=list(dict.items())
print(dict[0].keys())
print(dict[0].values())
print(dictlist)
#print(dictlist.index())

od = OrderedDict()
od['a'] = 1
od['b'] = 2
od['c'] = 3
od['d'] = 4
  
for key, value in od.items():
    print(key, value)
print("removing pair\n")

od.pop('c')
for key, value in od.items():
    print(key, value)
print('adding a pair')

od['c'] = 3
for key, value in od.items():
    print(key, value)