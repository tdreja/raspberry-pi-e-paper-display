from datetime import datetime

from google_integration.google_loader import monthly_events, monthly_holidays
from util.dateloader import load_holidays, load_events


def load_all_events(today=datetime.today()):
    year = today.year
    month = today.month

    local_holidays = load_holidays(year=year, month=month)
    local_events = load_events(year=year, month=month)
    google_events = monthly_events(year=year, month=month)
    google_holidays = monthly_holidays(year=year, month=month)
    print(google_holidays)

    return CalendarInfo(month=month, year=year, local_holidays=local_holidays, local_events=local_events,
                        google_holidays=google_holidays, google_events=google_events)


def filter_events_for_day(events=None, day=datetime.today()):
    if events is None:
        return []

    result = []
    for event in events:
        if event.is_at_day(day):
            result.append(event)

    return result


def filter_events_for_time(events=None, now=datetime.now()):
    if events is None:
        return []

    result = []
    for event in events:
        if event.is_currently_or_upcoming(now):
            result.append(event)

    return result


def already_exists(events=None, event=None):
    if event is None:
        return True

    if events is None:
        return False

    for other in events:
        if event.start_as_date() == other.start_as_date() and event.end_as_date() == other.end_as_date():
            return True
    return False


class CalendarInfo:
    def __init__(self, month=datetime.now().month, year=datetime.now().year, local_holidays=None, local_events=None,
                 google_holidays=None, google_events=None):
        self.month = month
        self.year = year
        self.events = []
        self.holidays = []
        self.append_events(local_holidays)
        self.append_events(local_events)
        self.append_events(google_holidays)
        self.append_events(google_events)

    def append_events(self, events=None):
        if events is None:
            return

        for event in events:
            self.append_event(event)

    def append_event(self, event=None):
        if event is None:
            return
        elif not event.is_in_year_and_month(self.year, self.month):
            return
        elif event.is_holiday():
            if already_exists(self.holidays, event):
                return
            self.holidays.append(event)
        else:
            self.events.append(event)

    def list_holidays(self, day=datetime.today()):
        return list(map(lambda entry: entry.display(), filter_events_for_day(self.holidays, day)))

    def list_events(self, now=datetime.now()):
        return list(map(lambda entry: entry.display(), filter_events_for_time(self.events, now)))

    def is_holiday(self, day=datetime.today()):
        for holiday in self.holidays:
            if holiday.is_at_day(day):
                return True
        return False

    def is_whole_day_event(self, day=datetime.today()):
        for event in self.events:
            if event.is_whole_day() and event.is_at_day(day):
                return True
        return False

    def is_day_event(self, day=datetime.today()):
        for event in self.events:
            if not event.is_whole_day() and event.is_at_day(day):
                return True
        return False
