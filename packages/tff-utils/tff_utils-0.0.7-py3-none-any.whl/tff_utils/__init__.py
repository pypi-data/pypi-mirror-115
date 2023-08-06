import typing

from . import configuration, connection, k8s

__version__ = '0.0.7'


def initialize() -> None:
    options = configuration.parse()
    hosts: typing.List[str] = configuration.get_hosts(options=options)
    ca_cert_path: str = options.ca_cert

    if not hosts:
        return
    k8s.notify_istio_proxy_quit_before_exit()
    configuration.startup_sleep()
    connection.initialize_grpc(hosts=hosts, ca_cert_path=ca_cert_path)
