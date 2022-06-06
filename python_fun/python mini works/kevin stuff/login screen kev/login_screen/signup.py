import clear
import json
from getpass import getpass as getpass

### CLASS SIGN UP ###
class signup_screen:

    def __init__(self):
        self.db_json = open('database.json','r')
        self.database = json.load(self.db_json)
        self.db_json.close()
        clear.clear()
        self.get_uname()
    
    def get_uname(self):
        print("SIGNUP\n")
        self.uname=input("Please create a username: ")
        while self.uname in self.database:
            clear.clear()
            print("SIGNUP\n")
            print("The username \'" + self.uname + "\' already exists!")
            self.uname=input("Please enter another name: ")
        self.get_pwd()
        
    def get_pwd(self):
        self.pwd=getpass("Please enter a password: ")
        self.pwd_copy=getpass("Please reenter the password: ")
        while (self.pwd != self.pwd_copy):
            print("\nThe entered password do not match. Please try again.")
            self.pwd=getpass("Please enter a password: ")
            self.pwd_copy=getpass("Please reenter the password: ")
        self.add_to_database()
        
    def add_to_database(self):
        self.database[self.uname]=(self.pwd)
        self.db_json=open('database.json',"w")
        json.dump(self.database,self.db_json)
        self.db_json.close()
        clear.clear()
        print("\nUser account created successfully. You can now login with your new account\n")         
### END CLASS SIGNUP ###        
