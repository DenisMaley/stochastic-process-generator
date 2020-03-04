import datetime
import threading

from nameko.rpc import rpc, RpcProxy


class TimeService:
    name = 'time_service'
    day_coef = [1, 1, 1, 1, 1, .75, .5]

    parameter_service = RpcProxy('parameter_service')

    # TODO implement timezones (Now let's leave only UTC for simplicity)
    @staticmethod
    def get_now():
        return datetime.datetime.utcnow()

    def get_today(self):
        now = self.get_now()
        return datetime.datetime(now.year, now.month, now.day)

    def set_timer(self, days: float, callback, *args, **kwargs):
        period = days * (24 * 60 * 60) / self.day_coef[self.get_today().weekday()]
        timer = threading.Timer(period, callback, args, kwargs)
        timer.start()

    # TODO Investigate how to pass callback without wrapping them in time_service
    @rpc
    def update_param_after(self, days):
        self.set_timer(days, self.parameter_service.update_param)
