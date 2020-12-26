import calendar
import locale
from datetime import date

from PIL import ImageFont, Image, ImageDraw

locale.setlocale(category=locale.LC_ALL, locale="German")

color_white = 255
color_black = 0

roboto16 = ImageFont.truetype('./Roboto-Bold.ttf', 16)
roboto12 = ImageFont.truetype('./Roboto-Regular.ttf', 12)
roboto14 = ImageFont.truetype('./Roboto-Medium.ttf', 14)
roboto24 = ImageFont.truetype('./Roboto-Bold.ttf', 24)

header_height = 80
headline_height = 48
small_padding = 6
padding = 8
col_width = 48
row_small = 32
row_full = 48

holidays = [date(2020, 12, 24), date(2020, 12, 25), date(2020, 12, 26)]


def create_calendar():
    today = date(2021, 2, 1)
    month = today.month
    year = today.year
    day = today.day
    text_calendar = calendar.TextCalendar(calendar.MONDAY)

    day_str = str.format("{}, der {}.{}.{}", calendar.day_name[today.weekday()], day, month, year)
    print(day_str)
    print(text_calendar.formatmonthname(year, month, 30))

    for week in text_calendar.monthdatescalendar(year, month):
        week_nr = week[0].isocalendar()[1]
        day_numbers = []
        for day in week:
            if day.month == month:
                day_numbers.append(day.day)
            else:
                day_numbers.append(0)

        weekdays = str.join(', ', map(str, day_numbers))
        print(str.format("Week #{} {}", week_nr, weekdays))

    for week in text_calendar.monthdayscalendar(year, month):
        weekdays = str.join(', ', map(str, week))
        print(str.format("Week {}", weekdays))


def draw_calendar(draw, start_coords, image_width, today=date.today()):
    month = today.month
    year = today.year
    text_calendar = calendar.TextCalendar(calendar.MONDAY)

    xy = start_coords
    draw_header(draw, xy, image_width, text_calendar, text_calendar.formatmonthname(year, month, 20))

    xy = (xy[0], xy[1] + header_height)
    draw_rows(draw, xy, month, weeks=text_calendar.monthdatescalendar(year, month), today=today)


def draw_header(draw, start_xy, image_width, text_calendar, headline):
    draw.rectangle((start_xy[0], start_xy[1],
                    start_xy[0] + image_width + 1, start_xy[1] + header_height + 1),
                   fill=color_black, outline=None, width=0)

    # Calendar Headline
    draw_text_centered(draw, xy=start_xy, size=(image_width, col_width),
                       text=headline, font=roboto24, color=color_white)

    # Column Headers
    column_xy = (start_xy[0], start_xy[1] + headline_height)
    draw_small_row_text(draw, column_xy, '#')

    # Print each weekday with 2 characters
    for weekDay in text_calendar.iterweekdays():
        column_xy = (column_xy[0] + col_width, column_xy[1])
        draw_small_row_text(draw, column_xy, text_calendar.formatweekday(weekDay, 2))


def draw_rows(draw, start_xy, month, weeks, today=date.today()):
    column_xy = start_xy
    for week in weeks:
        week_nr = week[0].isocalendar()[1]
        # Draw the week number
        draw_row_text(draw, column_xy, str(week_nr), font=roboto14)
        column_xy = (column_xy[0] + col_width, column_xy[1])
        underline_y = column_xy[1] + row_full - padding

        # Draw the days
        for day in week:
            font = roboto16
            color = color_black

            if day.month != month:
                font = roboto12

            if day == today:
                # Background
                color = color_white
                draw.rectangle((column_xy[0] + small_padding, column_xy[1] + small_padding,
                                column_xy[0] + col_width - small_padding + 1,
                                column_xy[1] + row_full - small_padding + 1),
                               fill=color_black, outline=None, width=0)

            if day in holidays:
                # Special Underline for holidays
                draw.line([column_xy[0] + padding, underline_y - 2,
                           column_xy[0] + col_width - padding, underline_y - 2],
                          width=1, fill=color)

                draw.line([column_xy[0] + padding, underline_y, column_xy[0] + col_width - padding, underline_y],
                          width=1, fill=color)

            elif day.weekday() == 5 or day.weekday() == 6:
                # Underline
                draw.line([column_xy[0] + padding, underline_y, column_xy[0] + col_width - padding, underline_y],
                          width=1, fill=color)

            draw_row_text(draw, column_xy, str(day.day), font=font, color=color)
            column_xy = (column_xy[0] + col_width, column_xy[1])

        # At the end reset the coordinates
        column_xy = (start_xy[0], column_xy[1] + row_full)


def draw_row_text(draw, xy, text, font=roboto16, color=color_black):
    draw_text_centered(draw, xy, text, font, color, size=(col_width, row_full))


def draw_small_row_text(draw, xy, text):
    draw_text_centered(draw, xy, text, font=roboto14, color=color_white, size=(col_width, row_small))


def draw_text_centered(draw, xy, text, font, color=0, size=(0, 0)):
    text = text.strip()
    text_size = draw.textsize(text, font=font)
    offset_x = (size[0] - text_size[0]) / 2
    offset_y = (size[1] - text_size[1]) / 2
    draw.text((xy[0] + offset_x, xy[1] + offset_y), text, font=font, fill=color)


def test_calendar(width, height, today=date.today()):
    image = Image.new('1', (width, height), 255)
    draw = ImageDraw.Draw(image)

    draw_calendar(draw, (0, 0), width, today)

    # write to stdout
    image.show()


test_calendar(384, 640)
