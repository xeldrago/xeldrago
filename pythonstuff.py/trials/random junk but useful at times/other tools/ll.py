Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:21:23) [MSC v.1916 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> def dm():
    status = input("are u known y/n? press q to get out")
    if status == "y":
        ou()
    elif status == "n":
        nu()

def nu():
    createLogin = input("Create login name: ")

    if createLogin in users:
        print("\nchoose another name bro!\n")
    else:
        createPassw = input("Create password: ")
        users[createLogin] = createPassw
        print("\nUser created\n")

def ou():
    login = input("Enter login name: ")
    passw = input("Enter password: ")

    if login in users and users[login] == passw:
        print("\nyour in, now go hafun exiting\n")
    else:
        print("\nur not known here jus get out\n")

while status != "q":
    dm()
