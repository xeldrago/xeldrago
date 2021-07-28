import clear
import json
from getpass import getpass as getpass

### CLASS LOGIN ###
class login_screen:
    
    def __init__(self):
        self.db_json = open('database.json','r')
        self.database = json.load(self.db_json)
        self.db_json.close()
        clear.clear()
        self.get_uname()
        
        
    def get_uname(self):
        print("LOGIN\n")
        self.uname=input("Please enter your username: ")
        while self.uname not in self.database:
            clear.clear()
            print("LOGIN\n")
            self.uname = input("This user does not exist! \nPlease try again: ")
        self.get_pwd()
        
    def get_pwd(self):
        self.pwd=getpass("Please enter your password: ")
        while self.pwd != self.database.get(self.uname):
            self.result=0
            self.pwd = getpass("Entered password does not match username " + self.uname + "!\nPlease try again: ")
        self.result=1
### END CLASS LOGIN###  

### LOGIN MENU ###
def login_menu():
    while True:
        print("Welcome to Project Program 1\n")
        print("Returning user? \n\tType 1 to login to your account!")
        print("New user? \n\tType 2 to create your account!")
        print("Wanna get outta here? \n\tType 3 to exit")
        choice=input("\nYour choice: ")
        
        if (choice > "0" and choice < "4"):
            return int(choice)
        else:
            clear.clear()
            print("Invalid choice\n")
### END LOGIN MENU 
