import os
from datetime import date


def load_events(month, year):
    return load_dates_from_file(month, year, '../events_'+str(year)+'-'+str(month)+'.csv')


def load_holidays(month, year):
    return load_dates_from_file(month, year, '../holidays_'+str(year)+'.csv')


def parse_date(year, line):
    split = line.split(";")
    parsed = date.fromisoformat(split[0])
    if parsed.year == year:
        return parsed, split[1]
    if parsed.year == 0:
        return date(year, parsed.month, parsed.day), split[1]


def load_dates_from_file(month, year, file):
    dates = []
    if not os.path.exists(file):
        return dates

    f = open(file)
    for line in f.readlines():
        parsed = parse_date(year, line)
        if parsed[0].month == month:
            dates.append(parsed)
    f.close()
    return dates
