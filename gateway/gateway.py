import json

from nameko.rpc import RpcProxy
from nameko.web.handlers import http


class GatewayService:
    name = 'gateway'

    parameter_service = RpcProxy('parameter_service')

    @http('GET', '/parameter')
    def get_parameter(self, request):
        parameter = self.parameter_service.get_param()
        return json.dumps({'parameter': parameter})

    @http('POST', '/process')
    def post_process(self, request):
        data_as_text = request.get_data(as_text=True)

        try:
            data = json.loads(data_as_text)
        except json.JSONDecodeError:
            return 400, 'JSON payload expected'

        try:
            trigger = int(data['trigger'])
        except KeyError:
            return 400, 'No message given'

        self.parameter_service.set_process_triggered(trigger)

        return 200, ''
