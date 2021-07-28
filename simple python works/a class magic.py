class computer:
    def __init__(self,a,b,c,d):
        self.part1=a
        self.part2=b
        self.part3=c
        self.part4=d
    def desktop(self):
        
        print("desktop needs all four parts seperately,",self.part1,',is seperate as well as the other three',"\n",self.part2,"\n",self.part3,"\n",self.part4)
        


class laptop(computer):
    def __init__(self,a,b,c='none',d='none'):
        super().__init__(a,b,c,d)
        print("laptop has all built-into one")
        all_in_one=self.part1+self.part2+self.part3+self.part4
        print(all_in_one)
a=input('name the parts of a computer,part1:')
b=input('part2:')
c=input('part3:')
d=input('part4:')
c1=computer(a,b,c,d)
c1.desktop()
r1=laptop(a,b,c,d)

