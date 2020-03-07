from envyaml import EnvYAML
from nameko.standalone.rpc import ServiceRpcProxy

config = EnvYAML('config.yml')

with ServiceRpcProxy("parameter_service", config) as parameter_service:
    parameter_service.schedule_update_param()
