import locale
from datetime import datetime

from PIL import Image, ImageDraw

from drawcalendar.drawcalendar import draw_calendar
from drawtoday.drawtoday import draw_today, full_height
from util.calendar_info import load_all_events

locale.setlocale(category=locale.LC_ALL, locale='de_DE.UTF-8')


def full_test(width, height, today=datetime.now()):
    image = Image.new('1', (width, height), 255)
    draw = ImageDraw.Draw(image)
    calendar_info = load_all_events(today)

    draw_today(draw, (0, 0), width, today, calendar_info)
    draw_calendar(draw, (0, full_height), width, today.date(), calendar_info)

    # image = image.rotate(angle=90, expand=1)

    # write to stdout
    image.show()


full_test(384, 640)
