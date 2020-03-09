import json

from nameko.rpc import RpcProxy
from nameko.web.handlers import http


class GatewayService:
    name = 'gateway'

    parameter_service = RpcProxy('parameter_service')

    @http('GET', '/parameter')
    def get_parameter(self):
        parameter = self.parameter_service.get_param()
        return json.dumps({'parameter': parameter})