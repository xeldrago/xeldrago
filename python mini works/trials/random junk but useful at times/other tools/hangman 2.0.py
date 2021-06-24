words = {"t","h","o","r"}
answer = set()
counter = 0
def game():
    global counter
    guess = input("guess a letter:")
    for letter in words:
        #print (letter)
        if guess in letter:
            print("yes")
            answer.add(guess)
            print(answer)
            counter += 1
            print(counter)
        elif guess not in letter:
            print ("no")
            counter +=1
        
while answer != words:
    game()
else:
    print("you win")
    
