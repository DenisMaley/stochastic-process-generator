import numpy as np
from nameko.events import EventDispatcher
from nameko.rpc import rpc, RpcProxy
from nameko_redis import Redis


class ParameterService:
    name = 'parameter_service'

    param_name = 'p'
    init_param = 0

    time_service = RpcProxy('time_service')

    dispatch = EventDispatcher()

    redis = Redis('development')

    # TODO: subscribe to listen update_param
    @rpc
    def schedule_update_param(self) -> bool:
        r = np.random.uniform(0, 0.0002)
        self.time_service.update_param_after(r)

        return True

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
