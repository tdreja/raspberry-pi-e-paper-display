import calendar
import locale
from datetime import date

locale.setlocale(category=locale.LC_ALL, locale="German")


def create_calendar():
    today = date(2020, 11, 1)
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




create_calendar()
