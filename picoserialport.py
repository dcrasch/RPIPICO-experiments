import board
import busio
import time
uart = busio.UART(board.GP0, board.GP1, baudrate=115200)
while True:
    uart.write(b"Hello pico world\r\n")
    time.sleep(1)
