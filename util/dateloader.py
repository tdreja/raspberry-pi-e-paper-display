import os
from datetime import date


def load_events(month, year):
    return load_dates_from_file(month, year, './events_' + str(year) + '_' + str(month) + '.csv')


def load_holidays(month, year):
    return load_dates_from_file(month, year, './holidays_' + str(year) + '.csv')


def load_event_names(today=date.today()):
    events = filter(lambda event_tuple: event_tuple[0] == today, load_events(today.month, today.year))
    return list(map(lambda event_tuple: event_tuple[1], events))


def load_holiday_names(today=date.today()):
    holidays = filter(lambda event_tuple: event_tuple[0] == today, load_holidays(today.month, today.year))
    return list(map(lambda event_tuple: event_tuple[1], holidays))


def parse_date(year, line):
    split = line.split(":", 1)
    parsed = date.fromisoformat(split[0])
    if parsed.year == year:
        return parsed, split[1].strip()
    if parsed.year == 0:
        return date(year, parsed.month, parsed.day), split[1]


def load_dates_from_file(month, year, file):
    dates = []
    if not os.path.exists(file):
        return dates

    f = open(file, encoding="utf-8")
    for line in f.readlines():
        parsed = parse_date(year, line)
        if parsed[0].month == month:
            dates.append(parsed)
    f.close()
    return dates
