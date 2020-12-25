#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
from waveshare_epd import epd7in5
import time
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd7in5 Demo")
    
    epd = epd7in5.EPD()
    logging.info("init and Clear")
    epd.init()
    #epd.Clear()
    
    logging.info("3.read bmp file")
    Himage = Image.open('test.bmp')
    epd.display(epd.getbuffer(Himage))
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
