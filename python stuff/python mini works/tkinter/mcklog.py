from tkinter import *
from functools import partial

def Login(username, password):
	print("username entered :", username.get())
	print("password entered :", password.get())
	


Window = Tk()  
Window.geometry('500x200')
Window.configure(bg='black')
Window.title('Login')
Label(Window,bg='White', text="Please enter the login details").pack()
Label(Window,bg='blue',fg='white', text="User Name").pack()
username = StringVar()
Entry(Window, textvariable=username).pack() 
Label(Window,bg='blue',fg='white',text="Password").pack()  
password = StringVar()
Entry(Window, textvariable=password, show='*').pack() 

Login = partial(Login, username, password)

loginButton = Button(Window,bg='cyan', text="Login", command=Login).pack()

Window.mainloop()
