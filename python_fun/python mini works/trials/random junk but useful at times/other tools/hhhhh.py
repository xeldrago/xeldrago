
def state():

 state = input("are u known y/n ,to exit press q===")
 if state == "y":
      oldguy()
      print ("hi man ur inside the menu")
 elif state == "n":
       newguy()
       print("u can login known guy")
def oldguy():
    input("olduser namer;")
    input("old pasword=")
def newguy():
    input("new user name:")
    input("password:")
while state != "q":
    state()
    


    
