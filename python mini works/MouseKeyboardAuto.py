import mouse
import keyboard
#KR=keyboard.record(until='esc')
#play=keyboard.play(KR, speed_factor=2)
records=mouse.record()

a=0
while a != 10:
    a=a+1
    #mouse.click('left')
    mouse.play(records[:-1], speed_factor=1.0, include_clicks=True, include_moves=True, include_wheel=True)#press right click to start playing after u do ur jiggle or work
      
#mouse.unhook_all()

