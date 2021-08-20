import random
import string
import os
from typing import Text
import pyautogui as pya
try:
    passlen=int(input("tell the length of password you want:\n"))

    
    all=string.ascii_lowercase+string.ascii_uppercase+string.digits+string.punctuation
 
    passGen = random.sample(all,passlen)
    password = "".join(passGen)
    print(password)
    os.system(f'echo "{password}" >> PassWords.txt')
    pya.confirm(text="hey the Password is made and stored in passwords file", title="Password Generation Successful", buttons=['OK', 'Cancel'])
except:
    print("oops somthing was messed up")
    input("you sure you dint ask for a password above 150 charecters?\n")
    print("jus get out bruh.. u lying, try re running")
    
