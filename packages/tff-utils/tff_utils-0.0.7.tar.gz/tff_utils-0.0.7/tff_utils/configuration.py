import os
import time
import typing

import configargparse


def get_hosts(options: configargparse.Namespace) -> typing.List[str]:
    host_option: typing.List[str] = options.host
    if host_option:
        return host_option
    hosts_option = options.hosts.split(',')
    if len(hosts_option) == 1 and hosts_option[0] == '':
        return []
    return hosts_option


def startup_sleep():
    secs = int(os.getenv('STARTUP_SLEEPING_SECONDS', '3'))
    time.sleep(secs=secs)


def parse() -> configargparse.Namespace:
    p = configargparse.ArgParser()
    p.add('-c', '--config', required=False, is_config_file=True, help='config file path')
    p.add('--host', action='append', default=[], help='remote host address, simulate training if not set')
    p.add(
        '--hosts',
        default='',
        help='remote host address, simulate training if not set, seperated by commas',
        env_var='WOKER_HOSTS',
    )
    p.add('--ca-cert', default='', help='CA cert path')
    return p.parse_args()


if __name__ == '__main__':
    options = parse()
    print(options)
