import os 
def helloworld():
 helloworld = input("hi how are u")
 typesofreplies = "hi" or "hi im fine" or "oh hi" or "who are u" or "how are u doing?" or "im fine,how are u" or "" 
 if helloworld in typesofreplies:
    print("my name is jeff")
    input("what is your sweet name")
    if input != 0:
        a = "thanks" or "nice to meet u too" or "likevise"
        print("tht is a lovely name")
        d = input("glad to meet u")
        if d in a:
            print("ok carry on ,looking forward to work with u")
        else:
            p = input("say somthing that is in my data plse")
            if p in a:
                print("ok carry on ,looking forward to work with u")
            else:
                print("im sry i cant understand but.. thnks for talking to me!")
                

    else:
        print("wow a nice name indeed,glad to meet u")
 else:
    print("im not gonna reply tht ,type somthing tht i know how to reply for")
    helloworld()
    
helloworld()

os.system("pause")