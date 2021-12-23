import board
import busio
import digitalio
import adafruit_sdcard
import storage
import os
import adafruit_framebuf
from adafruit_is31fl3731.matrix import Matrix as Display

i2c = busio.I2C(scl=board.GP1,sda=board.GP0)
display = Display(i2c)
display.fill(0)

spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP4)
# Use board.SD_CS for Feather M0 Adalogger
cs = digitalio.DigitalInOut(board.GP5)
# Or use a digitalio pin like 5 for breakout wiring:
#cs = digitalio.DigitalInOut(board.D5)

sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

with open("/sd/test.txt", "w") as f:
    f.write("""AAa""")
    
with open("/sd/test.txt", "r") as f:
    lines = f.read()
    
text_to_show = lines

# Create a framebuffer for our display
buf = bytearray(32)  # 2 bytes tall x 16 wide = 32 bytes (9 bits is 2 bytes)
fb = adafruit_framebuf.FrameBuffer(
    buf, display.width, display.height, adafruit_framebuf.MVLSB
)


frame = 0  # start with frame 0
while True:
    for i in range(len(text_to_show) * 9):
        fb.fill(0)
        fb.text(text_to_show, -i + display.width, 0, color=1)

        # to improve the display flicker we can use two frame
        # fill the next frame with scrolling text, then
        # show it.
        display.frame(frame, show=False)
        # turn all LEDs off
        display.fill(0)
        for x in range(display.width):
            # using the FrameBuffer text result
            bite = buf[x]
            for y in range(display.height):
                bit = 1 << y & bite
                # if bit > 0 then set the pixel brightness
                if bit:
                    display.pixel(x, y, 50)

        # now that the frame is filled, show it.
        display.frame(frame, show=True)
        frame = 0 if frame else 1
