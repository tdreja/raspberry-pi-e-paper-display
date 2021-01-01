import locale
import logging
import time
from datetime import datetime

import schedule
from PIL import Image, ImageDraw

from drawcalendar.drawcalendar import draw_calendar
from drawtoday.drawtoday import draw_today, full_height

locale.setlocale(category=locale.LC_ALL, locale='de_DE.UTF-8')


def do_schedule():
    full_test(384, 640)


def full_test(width, height, today=datetime.now()):
    print('draw calendar')
    image = Image.new('1', (width, height), 255)
    draw = ImageDraw.Draw(image)

    draw_today(draw, (0, 0), width, today)
    draw_calendar(draw, (0, full_height), width, today.date())

    # image = image.rotate(angle=90, expand=1)

    # write to stdout
    image.show()


schedule.every(5).seconds.do(do_schedule)

while True:
    try:
        schedule.run_pending()
        time.sleep(10)
    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        exit()
