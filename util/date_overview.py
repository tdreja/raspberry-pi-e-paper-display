from datetime import date, datetime


class DateOverview:

    def __init__(self, date_info=None):
        if date_info is None:
            date_info = []
        self.date_info = date_info

    def add_info(self, new_info=None):
        if new_info is None:
            pass
        self.date_info.append(new_info)

    def get_info(self):
        return self.date_info


class DateInfo:

    def __init__(self, name="", start_date=date.today(), end_date=date.today(), start_date_time=datetime.today(),
                 end_date_time=datetime.today()):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time

    def display(self):
        if self.is_whole_day():
            return self.name
        else:
            return self.name + self.start_time().isoformat() + self.end_time().isoformat()

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
