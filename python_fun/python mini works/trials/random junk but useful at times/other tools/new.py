users = {}
status = ""

def displayMenu():
    global status
    status = input("are u known y/n? press q to get out")
    if status == "y":
        oldUser()
    elif status == "n":
        newUser()
    elif status == "q":
        return
    else:
        print("get the f out dear")
def newUser():
    createLogin = input("Create login name: ")

    if createLogin in users:
        print("\nchoose another name bro!\n")
    else:
        createPassw = input("Create password: ")
        users[createLogin] = createPassw
        print("\nUser created\n")

def oldUser():
    login = input("Enter login name: ")
    passw = input("Enter password: ")

    if login in users and users[login] == passw:
        print("\nyour in, now go hafun exiting\n")
    else:
        print("\nur not known here jus get out\n")

while status != "q":
    displayMenu()
    #break

print("ur out of the login system ,die")   

