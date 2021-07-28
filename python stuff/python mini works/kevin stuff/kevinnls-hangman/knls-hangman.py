from distutils.core import setup
import py2exe
import json
from string import ascii_lowercase
#from string import ascii_uppercase
#from string import lower
from random import choice
from clear import clear
setup(console=['knls-hangman.py'])​
def listify(string):
    #n = 0
    l = []
    for i in string:
        l.append(i)
        #n+=1
    return l
def dashify(dashes):
    for i in dashes:
        print(i ,end = " ")
    print ("\n")
def top():
    clear()
    print("welcome to hangman\n")
    dashify(dashes)
    #print(len(dictionary))
    #print(len(completed))
    #print(completed)
    print("clue: " + clue)
def top_loss():
    clear()
    print("welcome to hangman\n")
    dashify(dashes)
    dashify(word)
    print("clue: " + clue)

### start hangman ###
def hangman():
    cache = []
    global dictionary
    global word
    global clue
    global dashes
    global completed
    chances = 6   
    
    if len(completed) == len(dictionary)+1:
       clear()
       print("thank you for playing hangman\n")
       print("you have beat the game. our dictionary has been exhausted. congrats!")
       exit()
    	
    else:	
        while word in completed:
            pick = choice(list(dictionary.items()))
            word = pick[0]
            clue = pick[1]
            del pick
        completed.append(word)
    wordx = listify(word)
    dashes = listify("_" * len(word))    
    top()
    print("\n")

    while dashes != wordx and chances>0:
    
        print("used letters: " + str(cache))
        print("chances left: " + str(chances) +"/6")
        guess = input("guess a letter: ")
        guess = guess.lower()
    
    ###tracking used letters###
        if len(guess)>1 or guess == '' :
            top()
            print("\ntype one letter at a time please\n")
            continue
        elif guess not in list(ascii_lowercase):
            top()
            print("\ntype only letters please\n")
            continue
        elif guess in cache:
            top()
            print("\nthis letter has already been used\n")
            continue
        elif guess not in cache:
            cache.append(guess)   
    ###tracking used letters###
    
    ###check letter in word###
        if guess in wordx:
            n=-1
            for i in wordx:
                n+=1
                if guess == i:
                    dashes[n] = wordx[n]
            top()
            print("\n")
         
        elif guess not in wordx:
            chances-=1
            top()
            print("\nthat letter is not in the word\n")
    
    if chances>0:
        top()

        print("\ncongrats! you have won!")
        return
    else:
        top_loss()
        print("\nsorry. you have lost.")
        return
### end hangman() ###

with open('dictionary.json') as dictf:
        dictionary = json.load(dictf)
        dictf.close()
dashes = ''
clue = ''
word = 'null' 
completed = ['null']

while True:
    hangman()
    
    replay = input("wanna play again? y/n: ")
    if replay == 'y':
        continue     
    elif replay == 'n':
        print("thanks! bye bye!")
        exit()
    else:
        print("invalid choice")
        continue
        
