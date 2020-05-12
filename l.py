from machine import UART, Pin, PWM
import neopixel
from time import sleep
# from clist import *
# from crc16 import crc16xmodem
# from aswitch import Pushbutton
# import uasyncio as asyncio
# import asyncio
# from debounce import DebouncedSwitch

print('Lasertag v2')
# GPIO Number:
PIN_BTN_PEW = 35  # 0 37 anderer pin gegen GND
PIN_IR_PWM = 25  # 25
PIN_SK9822 = 19  # 19
UART_NR = 2  # (0-2) (UART0 is used for serial REPL and, at the moment, is not available in this class.)
PIN_IR_TX = 32  # 1 U0TX
PIN_IR_RX = 4  # 3 U0RX

# loop = asyncio.get_event_loop()

# ----------------------- display -----------------------

# https://docs.badge.team/esp32-app-development/api-reference/display/
import display
display.flush()

display.drawFill(0x000000)
display.drawText(10, 10, "LaserTag 2 :D", 0xFFFF00, "permanentmarker22")
display.flush()

# ----------------------- led -----------------------

# https://docs.badge.team/esp32-app-development/api-reference/neopixel/
print('Set LEDs:')
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

# ----------------------- ir uart -----------------------

# rx_buffer = CircularList(4, [b'', b'', b'', b''])


# async def blink(n, wait_ms, color=neopixel.BLACK, white=10):
#     for i in range(n):
#         leds.set(1, color, white=white, num=5, update=True)
#         await asyncio.sleep_ms(wait_ms)  # Pause 1s
#         leds.set(1, neopixel.BLACK, white=0, num=5, update=True)
#         await asyncio.sleep_ms(wait_ms)  # Pause 1s


count_hit = 0
count_rx_bytes = 0


def uart_rx_event(res):  # res = (uart_num, 1, received_string)
    # triggered on every incoming byte; shift bytes through buffer of length of a valid hit; valid hit: 3 bytes: player_id, damage, crc8
    global count_rx_bytes  #, count_hit, rx_buffer
    count_rx_bytes += 1
    print('RXY', count_rx_bytes)
    # tft.text(tft.CENTER, 210, 'hit: ' + str(count_hit), tft.WHITE, transparent=True)
    # uartnr, length, data = res  # type(data) == str
    # rx_buffer.append(b"%c" % data)  # [b'!', b'?', b'\x06']; data-bytes, 1 checksum byte
    # # print('rx:', int.from_bytes(data, 'little'), type(data), data, rx_buffer, time.ticks_ms())
    # checksum = int(crc16xmodem(b''.join(rx_buffer[:2]))).to_bytes(2, 'little')  # [b'!', b'?'] --> b'!?'; calc crc8 of potential data-bytes
    # print('RX', count_rx_bytes)  # , ':', b"%c" % data, 'crc16 berechnet:', checksum, 'empfangen:', b''.join(rx_buffer[-2:])
    # if checksum == b''.join(rx_buffer[-2:]):  # if crc == last byte of buffer --> valid hit!
    #     count_hit += 1
    #     print('Hit! player_id:', int.from_bytes(rx_buffer[0], 'little'), 'damage:', int.from_bytes(rx_buffer[1], 'little'))  # , 'time_ms:', time.ticks_ms()
    #     tft.text(tft.CENTER, 120, 'hit: ' + str(count_hit), tft.YELLOW, transparent=False)
    #     loop.create_task(blink(n=1, wait_ms=8, white=200))
    #     loop.create_task(blink(n=1, wait_ms=4, white=100))


uart = UART(UART_NR, tx=PIN_IR_TX, rx=PIN_IR_RX, timeout=5000, buffer_size=32, baudrate=1200)
# uart = UART(1, tx=33, rx=35, timeout=5000, buffer_size=32, baudrate=1200)
uart.callback(uart.CBTYPE_DATA, func=uart_rx_event, data_len=1)

while 1:
    pass

# irsend = PWM(Pin(PIN_IR_PWM), freq=38000, duty=40.0)
# PWM.list()


# def uart_send(player_id, damage):
#     daten = b"%c%c" % (player_id, damage)
#     # daten = int(player_id).to_bytes(1, 'little') + int(damage).to_bytes(1, 'little')
#     checksum = int(crc16xmodem(daten)).to_bytes(2, 'little')  # [b'!', b'?'] --> b'!?'; calc crc8 of potential data-bytes
#     # print('TX:', daten, checksum)
#     print('TX - Daten: ' + str(daten) + ' Chksm:' + str(checksum), len(daten + checksum))
#     uart.write(daten + checksum)  # IR send



# ----------------------- keys -----------------------

# Pin(37, Pin.OUT).value(0)  # virtual gnd for key

# count_shoot = 0
#
# def key1_event(art):  # fire!
#     # print("Key pressed: Fire!", art)
#     global count_shoot  # , player_id
#     count_shoot += 1
#     # tft.text(tft.CENTER, 180, 'shoot: ' + str(count_shoot), tft.WHITE, transparent=True)
#     player_id = 33
#     damage = 63
#     print('key1_event')
#     # print('Shoot! player_id:', player_id, 'damage:', damage, 'count_shoot:', count_shoot)#, 'time_ms:', time.ticks_ms()
#     tft.text(tft.CENTER, 90, 'shoot: ' + str(count_shoot), tft.YELLOW, transparent=False)
#     uart_send(player_id=player_id, damage=damage)
#
#
# key1 = Pushbutton(Pin(PIN_BTN_PEW, Pin.IN))  # , Pin.PULL_UP
# key1.press_func(key1_event, ('press',))
# print('init complete, entering asyncio-loop')
# tft.text(tft.CENTER, 60, 'entering loop...', tft.WHITE, transparent=True)
# loop.create_task(blink(10000000, 400, color=neopixel.RED, white=0))
# loop.run_forever()

# key1 = DebouncedSwitch(Pin(27, Pin.IN, Pin.PULL_UP), key1_event, 1, delay=50, tid=0)




# def send_test():
#     while(1):
#         player_id = 33
#         damage = 63
#         print('')
#         print('sende:', player_id, damage, b"%c%c" % (player_id, damage), time.ticks_ms())
#         uart_send(player_id=player_id, damage=damage)
#         while()
#         # uart_send(player_id=5, damage=111)
#         # sleep(1)


# send_test()
# print('bbb')




