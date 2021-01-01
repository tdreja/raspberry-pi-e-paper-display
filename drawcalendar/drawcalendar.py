import locale
import calendar
from datetime import date

from PIL import ImageFont, Image, ImageDraw
from dateloader import load_holidays

locale.setlocale(category=locale.LC_ALL, locale="German")

color_white = 255
color_black = 0

roboto16 = ImageFont.truetype('../fonts/Roboto-Bold.ttf', 16)
roboto12 = ImageFont.truetype('../fonts/Roboto-Regular.ttf', 12)
roboto14 = ImageFont.truetype('../fonts/Roboto-Medium.ttf', 14)
roboto24 = ImageFont.truetype('../fonts/Roboto-Bold.ttf', 24)

header_height = 80
headline_height = 48
small_padding = 6
padding = 8
col_width = 48
row_small = 32
row_full = 48


def draw_calendar(draw, start_xy, image_width, today=date.today()):
    """
    Draws the entire drawcalendar2 below the coordinates
    :param draw: Image Draw
    :param start_xy: Coordinates
    :param image_width: Width of the image
    :param today: the current date
    :return: nothing
    """
    month = today.month
    year = today.year
    text_calendar = calendar.TextCalendar(calendar.MONDAY)
    # Create a list of all holidays for this month
    holidays = list(map(lambda entry: entry[0], load_holidays(month, year)))

    xy = start_xy
    draw_header(draw, xy, image_width, text_calendar, text_calendar.formatmonthname(year, month, 20))

    xy = (xy[0], xy[1] + header_height)
    draw_rows(draw, xy, month, weeks=text_calendar.monthdatescalendar(year, month), holidays=holidays, today=today)


def draw_header(draw, start_xy, image_width, text_calendar, headline):
    """
    Draws the drawcalendar2 header with month and year and below the headlines for the table
    :param draw: Image Draw
    :param start_xy: Coordinates
    :param image_width: Width of the image
    :param text_calendar: Text drawcalendar2 for printing the weekdays
    :param headline: headline of drawcalendar2 (month + year)
    :return: nothing
    """
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


def draw_rows(draw, start_xy, month, weeks, holidays, today=date.today()):
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

    #image = image.rotate(angle=90, expand=1)

    # write to stdout
    image.show()


test_calendar(384, 640)