import os
from datetime import date

from util.date_info import DateInfo


def load_events(month, year):
    return load_dates_from_file(month, year, './events_' + str(year) + '_' + str(month) + '.csv', False)


def load_holidays(month, year):
    return load_dates_from_file(month, year, './holidays_' + str(year) + '.csv', True)


def parse_date(year, line, holiday=False):
    split = line.split(":", 1)
    parsed = date.fromisoformat(split[0])
    if parsed.year == year:
        return DateInfo(name=split[1], start_date=parsed, end_date=parsed, start_date_time=None, end_date_time=None,
                        holiday=holiday)
    if parsed.year == 0:
        val = date(year, parsed.month, parsed.day)
        return DateInfo(name=split[1], start_date=val, end_date=val, start_date_time=None, end_date_time=None,
                        holiday=holiday)


def load_dates_from_file(month, year, file, holiday=False):
    dates = []
    if not os.path.exists(file):
        return dates

    f = open(file, encoding="utf-8")
    for line in f.readlines():
        parsed = parse_date(year, line, holiday)
        if parsed.start_date.month == month:
            dates.append(parsed)
    f.close()
    return dates
