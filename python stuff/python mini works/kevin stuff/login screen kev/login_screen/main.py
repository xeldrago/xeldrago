import clear
from login import *
from signup import *
from menu import *

### MAIN ###
while True:

    x = login_menu()
    if x == 1:
        l=login_screen()
        if l.result==1:
            print("\n\nCredentials Verified. Logging in")
            sleep(1.4)
            u=menu(l.uname)
    elif x == 2:
        s = signup_screen()
        del s
    elif x==3:
        clear()
        print("Hope the right digital streams guides you to your destination.")
        exit()        
### END MAIN ###
