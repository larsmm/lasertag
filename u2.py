from machine import UART

uart = UART(1, tx=13, rx=12, timeout=5000, baudrate=1200)

while(True):
    if uart.any():
        print(uart.read(1))
