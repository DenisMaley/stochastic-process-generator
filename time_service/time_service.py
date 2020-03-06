import datetime
import threading

from nameko.rpc import rpc, RpcProxy


class TimeService:
    name = "time_service"
    day_coef = [1, 1, 1, 1, 1, .75, .5]

    parameter_service = RpcProxy('parameter_service')

    # TODO implement timezones (Now let's leave only UTC for simplicity)
    @staticmethod
    def get_now():
        return datetime.datetime.utcnow()

    def get_today(self):
        now = self.get_now()
        return datetime.datetime(now.year, now.month, now.day)

    def get_end_of_year(self):
        now = self.get_now()
        return datetime.datetime(now.year + 1, 1, 1) - datetime.timedelta(1)

    @staticmethod
    def get_num_days_between(start: datetime, end: datetime, week_day: int) -> int:
        num_weeks, remainder = divmod((end - start).days, 7)
        if (week_day - start.weekday()) % 7 <= remainder:
            return num_weeks + 1
        else:
            return num_weeks

    def get_seconds_until_midnight(self, dt: datetime = None) -> int:
        dt = dt or self.get_now()
        this_day = datetime.datetime(dt.year, dt.month, dt.day)
        next_day = this_day + datetime.timedelta(1)

        return abs(next_day - dt).seconds

    def get_days_until_midnight(self, dt: datetime = None) -> float:
        dt = dt or self.get_now()
        this_day = datetime.datetime(dt.year, dt.month, dt.day)
        time_in_days = self.get_seconds_until_midnight(dt) / (24 * 60 * 60)

        return self.day_coef[this_day.weekday()] * time_in_days

    @rpc
    def get_time_left(self, dt: datetime = None, until_day: datetime = None) -> float:
        dt = dt or self.get_now()
        until_day = until_day or self.get_end_of_year()

        time_in_days = self.get_days_until_midnight(dt)

        # TODO Cache this_day and time_in_days. Makes sense to recalculate only when this_day != cache
        this_day = datetime.datetime(dt.year, dt.month, dt.day)
        next_day = this_day + datetime.timedelta(1)
        for i, coef in enumerate(self.day_coef):
            time_in_days += coef * self.get_num_days_between(next_day, until_day, i)

        return time_in_days

    def set_timer(self, days: float, callback, *args, **kwargs):
        period = days * (24 * 60 * 60) / self.day_coef[self.get_today().weekday()]
        timer = threading.Timer(period, callback, args, kwargs)
        timer.start()

    # TODO Investigate how to pass callback without wrapping them in time_service
    @rpc
    def update_param_after(self, days):
        self.set_timer(days, self.parameter_service.update_param)
