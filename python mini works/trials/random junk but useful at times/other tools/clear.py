from os import system, name 
from time import sleep 

# defining function clear()
def clear(): 

	# for windows 
	if name == 'nt': 
		_ = system('cls') 

	# for mac and linux
	else: 
		_ = system('clear') 
