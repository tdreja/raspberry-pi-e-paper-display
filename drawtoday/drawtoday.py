import calendar
from datetime import datetime

from font import fonts
from util import drawtext
from util.calendar_info import CalendarInfo
from util.drawtext import draw_text_centered

headline_height = 48
text_block_height = 28
block_offset = 8

full_height = headline_height + (6 * text_block_height) + (7 * block_offset)


def draw_date(draw, content_xy, block_size, now=datetime.now()):
    text_calendar = calendar.TextCalendar(calendar.MONDAY)

    today = '{dayname},'.format(dayname=text_calendar.formatweekday(now.weekday(), 20).strip())
    draw_text_centered(draw, content_xy, today, font=fonts.roboto22,
                       color=fonts.color_black, size=block_size)

    next_xy = (content_xy[0], content_xy[1] + block_size[1])
    date = 'der {day}. {monthyear}'.format(day=now.day,
                                           monthyear=text_calendar.formatmonthname(themonth=now.month, theyear=now.year,
                                                                                   width=20).strip())
    draw_text_centered(draw, next_xy, date, font=fonts.roboto22, color=fonts.color_black, size=block_size)


def calculate_day_time(now=datetime.now()):
    if now.hour >= 21 or now.hour < 5:
        return 'Nachts,'
    if now.hour < 9:
        return 'Morgens,'
    if now.hour < 11:
        return 'Vormittags,'
    if now.hour < 13:
        return 'Mittags,'
    if now.hour < 17:
        return 'Nachmittags,'
    return 'Abends,'


def calculate_time(now=datetime.now()):
    if now.minute < 3:
        return 'Punkt {uhr}'.format(uhr=calculate_hour_name(now.hour))
    if now.minute < 8:
        return 'Fünf nach {uhr}'.format(uhr=calculate_hour_name(now.hour))
    if now.minute < 13:
        return 'Zehn nach {uhr}'.format(uhr=calculate_hour_name(now.hour))
    if now.minute < 18:
        return 'Viertal nach {uhr}'.format(uhr=calculate_hour_name(now.hour))
    if now.minute < 23:
        return 'Zehn vor halb {uhr}'.format(uhr=calculate_hour_name(now.hour + 1))
    if now.minute < 28:
        return 'Fünf vor halb {uhr}'.format(uhr=calculate_hour_name(now.hour + 1))
    if now.minute < 33:
        return 'halb {uhr}'.format(uhr=calculate_hour_name(now.hour + 1))
    if now.minute < 38:
        return 'Fünf nach halb {uhr}'.format(uhr=calculate_hour_name(now.hour + 1))
    if now.minute < 43:
        return 'Zehn nach halb {uhr}'.format(uhr=calculate_hour_name(now.hour + 1))
    if now.minute < 48:
        return 'Dreiviertel {uhr}'.format(uhr=calculate_hour_name(now.hour + 1))
    if now.minute < 53:
        return 'Zehn vor {uhr}'.format(uhr=calculate_hour_name(now.hour + 1))
    if now.minute < 58:
        return 'Fünf vor {uhr}'.format(uhr=calculate_hour_name(now.hour + 1))
    return 'Punkt {uhr}'.format(uhr=calculate_hour_name(now.hour + 1))


def calculate_hour_name(hour=0):
    if hour > 12:
        hour = hour - 12

    if hour == 1:
        return 'Eins'
    if hour == 2:
        return 'Zwei'
    if hour == 3:
        return 'Drei'
    if hour == 4:
        return 'Vier'
    if hour == 5:
        return 'Fünf'
    if hour == 6:
        return 'Sechs'
    if hour == 7:
        return 'Sieben'
    if hour == 8:
        return 'Acht'
    if hour == 9:
        return 'Neun'
    if hour == 10:
        return 'Zehn'
    if hour == 11:
        return 'Elf'
    return 'Zwölf'


def draw_time(draw, content_xy, block_size, now=datetime.now()):
    daytime = calculate_day_time(now)
    draw_text_centered(draw, content_xy, daytime, font=fonts.roboto22, color=fonts.color_black, size=block_size)

    next_xy = (content_xy[0], content_xy[1] + block_size[1])
    time = calculate_time(now)
    draw_text_centered(draw, next_xy, time, font=fonts.roboto22, color=fonts.color_black, size=block_size)


def draw_events(draw, start_xy, end_xy, line_size, now=datetime.now(), info=CalendarInfo()):
    lines = []
    holiday_texts = info.list_holidays(now.date())
    event_texts = info.list_events(now)

    lines.extend(
        drawtext.generate_drawable_lines(draw, font=fonts.roboto16, prefix='', joiner=', ', text_parts=holiday_texts,
                                         width=line_size[0]))

    if event_texts:
        lines.extend(
            drawtext.generate_drawable_lines(draw, font=fonts.roboto16, prefix='Termine: ', joiner=', ',
                                             text_parts=event_texts, width=line_size[0]))
    else:
        lines.append('Heute gibt es keine Termine')

    drawtext.draw_lines_centered(draw, font=fonts.roboto16, lines=lines, start_xy=start_xy, end_xy=end_xy,
                                 color=fonts.color_black, line_size=line_size)


def draw_today(draw, start_xy, image_width, now=datetime.now(), info=CalendarInfo()):
    draw.rectangle((start_xy[0], start_xy[1],
                    start_xy[0] + image_width + 1, start_xy[1] + headline_height + 1),
                   fill=fonts.color_black, outline=None, width=0)

    draw_text_centered(draw, xy=start_xy, text='Heute', font=fonts.roboto24, color=fonts.color_white,
                       size=(image_width, headline_height))

    block_size = (image_width, text_block_height)
    content_xy = (start_xy[0], start_xy[1] + headline_height + block_offset)

    draw_date(draw, content_xy=content_xy, block_size=block_size, now=now)

    content_xy = (content_xy[0], content_xy[1] + 2 * block_size[1] + 2 * block_offset)

    draw_time(draw, content_xy=content_xy, block_size=block_size, now=now)

    content_xy = (content_xy[0], content_xy[1] + 2 * block_size[1] + block_offset)

    draw_events(draw, start_xy=content_xy, end_xy=(content_xy[0], content_xy[1] + 3 * text_block_height),
                line_size=block_size, now=now, info=info)
