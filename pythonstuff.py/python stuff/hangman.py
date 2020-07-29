secret_word = ["t","h","o","r"]
answer = []
guess = input("enter one of the letter u think is in the word=")
for letter in range(len(secret_word)):
      if guess in answer:
          print("correct letter")
          input("enter next =")
      elif guess not in answer:
         input("nope wrong try again=")
     
