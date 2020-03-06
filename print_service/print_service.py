from nameko.events import event_handler
from nameko.rpc import RpcProxy


class PrintService:
    name = "print_service"
    record_template = "Time left: {time:.5f},  Parameter: {param:.3f}\r\n"

    time_service = RpcProxy('time_service')

    @event_handler("parameter_service", "update_param_event")
    def log_record(self, param: float):
        time = self.time_service.get_time_left()

        f = open("log.txt", "a")
        f.write(self.record_template.format(time=time, param=param))
        f.close()
