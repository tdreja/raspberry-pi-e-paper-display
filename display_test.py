#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging

from drawcalendar import drawcalendar
from waveshare_epd import epd7in5
import time
from PIL import Image,ImageDraw

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd7in5 Demo")
    
    epd = epd7in5.EPD()
    logging.info("init and Clear")
    epd.init()
    #epd.Clear()
    
    logging.info("read png file")
    Himage = Image.open('test.png')
    epd.display(epd.getbuffer(Himage))
    time.sleep(2)

    logging.info("create drawcalendar2")
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(image)
    drawcalendar.draw_calendar(draw, (0, 0), epd.height)
    epd.display(epd.getbuffer(image.rotate(angle=90, expand=1)))
    time.sleep(2)
    
    logging.info("Goto Sleep...")
    epd.sleep()
    time.sleep(3)
    
    epd.Dev_exit()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5.epdconfig.module_exit()
    exit()
