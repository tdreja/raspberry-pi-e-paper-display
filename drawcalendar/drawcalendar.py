import calendar
from datetime import date

from font import fonts
from util.calendar_info import CalendarInfo
from util.drawtext import draw_text_centered

header_height = 80
headline_height = 48
small_padding = 6
padding = 8
col_width = 48
row_small = 32
row_full = 48
event_rectangle = 4
event_offset = 4


def draw_calendar(draw, start_xy, image_width, today=date.today(), info=CalendarInfo()):
    """
    Draws the entire drawcalendar2 below the coordinates
    :param info:
    :param draw: Image Draw
    :param start_xy: Coordinates
    :param image_width: Width of the image
    :param today: the current date
    :return: nothing
    """
    month = info.month
    year = info.year
    text_calendar = calendar.TextCalendar(calendar.MONDAY)

    xy = start_xy
    draw_header(draw, xy, image_width, text_calendar, text_calendar.formatmonthname(year, month, 20))

    xy = (xy[0], xy[1] + header_height)
    draw_rows(draw, xy, month, weeks=text_calendar.monthdatescalendar(year, month), info=info, today=today)


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
                   fill=fonts.color_black, outline=None, width=0)

    # Calendar Headline
    draw_text_centered(draw, xy=start_xy, size=(image_width, col_width),
                       text=headline, font=fonts.roboto24, color=fonts.color_white)

    # Column Headers
    column_xy = (start_xy[0], start_xy[1] + headline_height)
    draw_small_row_text(draw, column_xy, '#')

    # Print each weekday with 2 characters
    for weekDay in text_calendar.iterweekdays():
        column_xy = (column_xy[0] + col_width, column_xy[1])
        draw_small_row_text(draw, column_xy, text_calendar.formatweekday(weekDay, 2))


def draw_rows(draw, start_xy, month, weeks, info=CalendarInfo(), today=date.today()):
    column_xy = start_xy
    for week in weeks:
        week_nr = week[0].isocalendar()[1]
        # Draw the week number
        draw_row_text(draw, column_xy, str(week_nr), font=fonts.roboto14)
        column_xy = (column_xy[0] + col_width, column_xy[1])
        underline_y = column_xy[1] + row_full - padding

        # Draw the days
        for day in week:
            font = fonts.roboto16
            color = fonts.color_black

            if day.month != month:
                font = fonts.roboto12

            if day == today:
                x_1 = column_xy[0] + small_padding
                x_2 = column_xy[0] + col_width - small_padding + 1
                y_1 = column_xy[1] + small_padding
                y_2 = column_xy[1] + row_full - small_padding + 1
                # Background
                color = fonts.color_white
                draw.rectangle((x_1, y_1, x_2, y_2),
                               fill=fonts.color_black, outline=None, width=0)

            if info.is_holiday(day):
                x_1 = column_xy[0] + padding
                x_2 = column_xy[0] + col_width - padding
                y_1 = underline_y - 2
                # Special double Underline for holidays
                draw.line([x_1, y_1, x_2, y_1],
                          width=1, fill=color)
                draw.line([x_1, underline_y, x_2, underline_y],
                          width=1, fill=color)

            elif day.weekday() == 5 or day.weekday() == 6:
                x_1 = column_xy[0] + padding
                x_2 = column_xy[0] + col_width - padding
                # Underline
                draw.line([x_1, underline_y, x_2, underline_y],
                          width=1, fill=color)

            if info.is_whole_day_event(day) and day.month == month:
                x_1 = column_xy[0] + padding + event_offset
                x_2 = x_1 + event_rectangle
                y_1 = column_xy[1] + padding
                y_2 = y_1 + 2 * event_rectangle
                # Left rectangle
                draw.rectangle((x_1, y_1, x_2, y_2),
                               fill=color, outline=None, width=0)

            if info.is_day_event(day) and day.month == month:
                x_1 = column_xy[0] + col_width - padding - event_offset - event_rectangle
                x_2 = x_1 + event_rectangle
                y_1 = column_xy[1] + padding
                y_2 = y_1 + event_rectangle
                # Right rectangle
                draw.rectangle((x_1, y_1, x_2, y_2),
                               fill=color, outline=None, width=0)

            draw_row_text(draw, column_xy, str(day.day), font=font, color=color)
            column_xy = (column_xy[0] + col_width, column_xy[1])

        # At the end reset the coordinates
        column_xy = (start_xy[0], column_xy[1] + row_full)


def draw_row_text(draw, xy, text, font=fonts.roboto16, color=fonts.color_black):
    draw_text_centered(draw, xy, text, font, color, size=(col_width, row_full))


def draw_small_row_text(draw, xy, text):
    draw_text_centered(draw, xy, text, font=fonts.roboto14, color=fonts.color_white, size=(col_width, row_small))
