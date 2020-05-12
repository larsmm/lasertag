from machine import UART

# uart = UART(1, tx=13, rx=12, timeout=5000, buffer_size=512, baudrate=1200)

uart = UART(1, 1200)
uart.init(1200, bits=8, parity=None, stop=1)

while(True):
    if uart.any():
        print(uart.read(uart.any()))
