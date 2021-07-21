from gtts import gTTS
import os
mytext = 'hey yo this is some awesome shitee!'

TextFile = open("Example.txt", "r")#u can use this to locate any text file u wanted read as well
f=TextFile.read()
print(TextFile.read())
  
# Language in which you want to convert
language = 'en'
  
# Passing the text and language to the engine, 
# here we have marked slow=False. Which tells 
# the module that the converted audio should 
# have a high speed
FuncObject = gTTS(text=mytext, lang=language, slow=False)
FuncObject2 = gTTS(text=f, lang=language, slow=False)
  
# Saving the converted audio in a mp3 file named
# welcome 
FuncObject.save("TextToSpeech.mp3")
FuncObject2.save("TextFileToSpeech.mp3")
  
# Playing the converted file
os.system("TextToSpeech.mp3")
os.system("TextFileToSpeech.mp3")
print("its done, check the folder for the audio file now")