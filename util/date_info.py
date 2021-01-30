from datetime import date, datetime


def check_day(year, month, day):
    return day.year == year and day.month == month


def date_in_range(start, end, compare):
    return start <= compare <= end


def is_upcoming(start, end, compare):
    return start >= compare and end >= compare


def is_currently(start, end, compare):
    return start <= compare <= end


class DateInfo:

    def __init__(self, name="", start_date=date.today(), end_date=date.today(), start_date_time=datetime.today(),
                 end_date_time=datetime.today(), holiday=False):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.holiday = holiday

    def is_holiday(self):
        return self.holiday

    def __repr__(self):
        if self.is_whole_day():
            return self.name + '(' + self.start_date.isoformat() + ' - ' + self.end_date.isoformat() + ')'
        else:
            return self.name + '(' + self.start_date_time.isoformat() + ' - ' + self.start_date_time.isoformat() + ')'

    def display(self):
        if self.is_whole_day():
            return self.name
        else:
            return self.name + '(' + self.start_time().isoformat() + ' - ' + self.end_time().isoformat() + ')'

    def is_whole_day(self):
        return self.start_date_time is None

    def start_day(self):
        if self.start_date_time is None:
            return self.start_date
        else:
            return self.start_date_time.date()

    def start_time(self):
        if self.start_date_time is None:
            return None
        else:
            return self.start_date_time.time()

    def end_time(self):
        if self.end_date_time is None:
            return None
        else:
            return self.end_date_time.time()

    def end_day(self):
        if self.end_date_time is None:
            return self.end_date
        else:
            return self.end_date_time.date()

    def is_in_range(self, year, month):
        return check_day(year, month, self.start_day()) or check_day(year, month, self.end_day())

    def is_at_day(self, day=datetime.now().date()):
        return date_in_range(self.start_day(), self.end_day(), day)

    def is_currently_or_upcoming(self, date_time=datetime.now()):
        in_range = date_in_range(self.start_day(), self.end_day(), date_time.date())

        if self.is_whole_day():
            return in_range
        elif in_range:
            if self.start_date_time.tzinfo is not None:
                date_time = date_time.astimezone()
            return is_upcoming(self.start_date_time, self.end_date_time, date_time) or is_currently(
                self.start_date_time, self.end_date_time, date_time)
        else:
            return False
