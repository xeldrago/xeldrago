
import keyboard
DB = []
while True:

    a = keyboard.read_key()
    if a not in DB:
        DB.append(a)

    if a == "end":
        break

text_file = open(r'E:\Repos\vroom-vroom\python_fun\python mini works\KeyImpressions_rec\KeyIMPS.txt', 'w')
listing=str(DB)
my_string = listing
text_file.write(my_string)
text_file.close()



# Record events until 'esc' is pressed.
#recorded = keyboard.record(until='esc')
# Then replay back at three times the speed.
# keyboard.play(recorded, speed_factor=3



