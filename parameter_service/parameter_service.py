import numpy as np
from nameko.events import EventDispatcher
from nameko.rpc import rpc, RpcProxy
from nameko_redis import Redis


class ParameterService:
    name = 'parameter_service'

    process_triggered_name = 'process_triggered'

    param_name = 'p'
    init_param = 0

    time_service = RpcProxy('time_service')

    dispatch = EventDispatcher()

    redis = Redis('development')

    # TODO: subscribe to listen update_param
    @rpc
    def schedule_update_param(self) -> bool:
        process_triggered = bool(self.get_process_triggered())

        if process_triggered:
            r = np.random.uniform(0, 0.0002)
            self.time_service.update_param_after(r)

        return process_triggered

    @rpc
    def update_param(self) -> float:
        p = self.get_param() + np.random.uniform(0, 1)

        self.set_param(p)
        self.dispatch('update_param_event', p)
        self.schedule_update_param()

        return p

    @rpc
    def get_param(self) -> float:
        param = self.redis.get(self.param_name) or self.init_param
        return float(param)

    def set_param(self, param_value: float) -> float:
        self.redis.set(self.param_name, param_value)
        return param_value

    def get_process_triggered(self) -> int:
        process_triggered = self.redis.get(self.process_triggered_name)
        return int(process_triggered)

    @rpc
    def set_process_triggered(self, process_triggered: int) -> int:
        self.redis.set(self.process_triggered_name, process_triggered)
        return process_triggered

    @rpc
    def start_process(self):
        self.set_process_triggered(1)
        self.schedule_update_param()

    @rpc
    def stop_process(self):
        self.set_process_triggered(0)
