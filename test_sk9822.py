# https://docs.badge.team/esp32-app-development/api-reference/neopixel/

# Enable neopixel and set pin (19) in config.h

print('Test: Neopixel SK9822 RGBW LEDs')


import neopixel
from time import sleep

neopixel.enable()

neopixel.send(bytes([1, 0, 0, 0] + [0, 1, 0, 0] + [0, 0, 1, 0] + [0, 1, 1, 0] + [0, 0, 0, 1]))
sleep(0.25)
neopixel.send(bytes([0, 0, 0, 0]*5))
sleep(0.25)
neopixel.send(bytes([0, 1, 0, 0]*5))
sleep(0.25)
neopixel.send(bytes([0, 0, 1, 0]*5))
sleep(0.25)
neopixel.send(bytes([0, 0, 0, 1]*5))
sleep(0.25)
neopixel.send(bytes([0, 0, 0, 0]*5))

neopixel.disable()  # disable, not aufhoeren zu leuchten

print('done')
