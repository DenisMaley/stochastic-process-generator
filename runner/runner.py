from envyaml import EnvYAML
from nameko.standalone.rpc import ServiceRpcProxy

config = EnvYAML('config.yml')

with ServiceRpcProxy("parameter_service", config) as proxy:
    proxy.start_process()
