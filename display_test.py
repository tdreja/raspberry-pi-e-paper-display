#!/usr/bin/python
# -*- coding:utf-8 -*-
import locale
import logging
import time
from datetime import datetime

from PIL import Image, ImageDraw

from drawcalendar.drawcalendar import draw_calendar
from drawtoday.drawtoday import draw_today, full_height
from util.calendar_info import load_all_events
from waveshare_epd import epd7in5


locale.setlocale(category=locale.LC_ALL, locale='de_DE.UTF-8')
logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("create calendar @{time}".format(time=datetime.now()))

    epd = epd7in5.EPD()
    logging.info("init and Clear")
    epd.init()
    # epd.Clear()

    logging.info("create calendar image")
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(image)
    today = datetime.now()
    calendar_info = load_all_events(today)
    draw_today(draw, (0, 0), epd.height, today, calendar_info)
    draw_calendar(draw, (0, full_height), epd.height, today.date(), calendar_info)
    epd.display(epd.getbuffer(image.rotate(angle=90, expand=1)))
    time.sleep(2)
    epd.sleep()
    time.sleep(3)
    epd.Dev_exit()
    logging.info('end of calendar creation')

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in5.epdconfig.module_exit()
    exit()
