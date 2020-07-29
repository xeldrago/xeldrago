class product:
    deliveryCharge=50
    def __init__(self,nam="Teddy Bear",prc=500):
        self.name=nam
        self.price=prc
    def get_name(self):
        return self.name
    def get_price(self):
        return self.price + product.deliveryCharge
    def __str__(self):
        return "The {} will cost you Rs.{}.".format(self.get_name(),self.get_price())
class gift(product):
    
    def __init__(self,nam="Teddy Bear",prc=500,wrpch=100):
        super().__init__(nam="Teddy Bear",prc=500)
        self.wrpchs=wrpch
    def get_price(self):
        return self.price+product.deliveryCharge+self.wrpchs
e1=product('teddy bear',500)
print("The {} will cost you Rs.{}.".format(e1.get_name(),e1.get_price()))
s1=gift('teddy bear',500,150)
print("the {} will cost u about Rs.{}".format(s1.get_name(),s1.get_price()))
