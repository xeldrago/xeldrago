import pygame
import pyvjoy

import pyvjoy._sdk as _sdk

status = _sdk.GetVJDStatus(1)
print("vJoy status:", status)


# Initialize pygame
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    raise RuntimeError("No joystick detected. Connect your controller first!")

js = pygame.joystick.Joystick(0)
js.init()

print("Detected controller:", js.get_name())

# vJoy controller
j = pyvjoy.VJoyDevice(1)

CENTER = 16384
MAX = 16384

x_axis = 0
y_axis = 0

def send_stick(x, y):
    j.data.wAxisX = CENTER + int(x * MAX)
    j.data.wAxisY = CENTER + int(y * MAX)
    j.update()

print("D-Pad → Left Stick remapping active. (CTRL+C to quit)")

while True:
    pygame.event.pump()

    # D-pad returns (x, y) as tuple
    hat_x, hat_y = js.get_hat(0)

    # Pygame: up = 1, down = -1 (reverse of vJoy)
    x_axis = hat_x
    y_axis = -hat_y

    send_stick(x_axis, y_axis)
