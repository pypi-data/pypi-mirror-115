import atexit
import logging
from urllib import error, request

logger = logging.getLogger(__name__)


def notify_istio_proxy_quit():
    path = 'http://127.0.0.1:15020/quitquitquit'
    try:
        request.urlopen(request.Request(path, data=''.encode()))
    except error.URLError as e:
        logger.error(f'Quit Istio error: {e}')


def notify_istio_proxy_quit_before_exit():
    atexit.register(notify_istio_proxy_quit)
