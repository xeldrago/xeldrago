from gtts import gTTS
import os
from playsound import playsound
with open('name123.txt') as f:
    contents = f.read()
    print(contents)

audio='speech.mp3'
tts = gTTS(contents,lang='en',slow=False)
tts.save(audio)
playsound(audio)

