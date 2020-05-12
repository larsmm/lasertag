from machine import UART

def uart_rx_event(res):
    print(res)
    # try:
    #     uartnr, length, data = res  # type(data) == str
    #     rx_buffer.append(b"%c" % data)  # [b'!', b'?', b'\x06']; data-bytes, 1 checksum byte
    #     # print('rx:', int.from_bytes(data, 'little'), type(data), data, rx_buffer, time.ticks_ms())
    #     checksum = int(crc16xmodem(b''.join(rx_buffer[:2]))).to_bytes(2, 'little')  # [b'!', b'?'] --> b'!?'; calc crc8 of potential data-bytes
    # except Exception as e:
    #     print('except dings', e)
    #     print(res)
    #     print(rx_buffer[0])
    #     print(rx_buffer[1])
    #     print(rx_buffer[2])
    #     print(rx_buffer[3])
    # # print('RX:', b"%c" % data, 'crc16 berechnet:', checksum, 'empfangen:', b''.join(rx_buffer[-2:]))
    # # if checksum == b''.join(rx_buffer[-2:]):  # if crc == last byte of buffer --> valid hit!
    # #     print('Hit! player_id:', int.from_bytes(rx_buffer[0], 'little'), 'damage:', int.from_bytes(rx_buffer[1], 'little'), 'time_ms:', time.ticks_ms())

print('gaga')
	
# uart = UART(1, tx=13, rx=12, timeout=5000, buffer_size=32, baudrate=1200)
uart = UART(1, tx=13, rx=3, timeout=5000, buffer_size=32, baudrate=1200)
uart.callback(uart.CBTYPE_DATA, func=uart_rx_event, data_len=1)

print('gugu')
