from nameko_redis import Redis


class ParameterService:
    name = "parameter_service"

    param_name = 'p'
    init_param = 0

    redis = Redis('development')

    def get_param(self):
        param = self.redis.get(self.param_name) or self.init_param
        return float(param)

    def set_param(self, param_value: float) -> float:
        self.redis.set(self.param_name, param_value)
        return param_value
