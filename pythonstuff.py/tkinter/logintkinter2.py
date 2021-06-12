import tkinter as tk

screen = tk.Tk()
screen.geometry("250x300")
screen.title("Notes")
tk.Label(text = "Notes", bg = "grey", font = ("calibri", 13)).pack()
tk.Label(text = "").pack() 
tk.Button(text = "login").pack()
username=username.get()
password=password.get()
tk.Label(text = "").pack() 
tk.Button(text = "register").pack()
screen.mainloop()
 
