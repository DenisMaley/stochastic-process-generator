from envyaml import EnvYAML
from nameko.standalone.rpc import ServiceRpcProxy

config = EnvYAML('config.yml')

with ServiceRpcProxy("parameter_service", config) as proxy:
    proxy.set_process_triggered(1)
    proxy.schedule_update_param()
