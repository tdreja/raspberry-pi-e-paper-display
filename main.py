import time
import traceback

from PIL import Image, ImageDraw, ImageFont

import epd7in5

try:
    epd = epd7in5.EPD()
    epd.init()
    print("Clear")
    epd.Clear(0xFF)

    print("read bmp file")
    Himage = Image.open('7in5.bmp')
    epd.display(epd.getbuffer(Himage))
    time.sleep(2)

    epd.sleep()

except:
    print('traceback.format_exc():\n%s', traceback.format_exc())
    exit()
