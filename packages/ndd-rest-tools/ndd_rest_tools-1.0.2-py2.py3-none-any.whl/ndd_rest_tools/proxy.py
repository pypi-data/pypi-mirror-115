from .models import ProxyModel
import os


def add_proxy(config: ProxyModel):
    os.environ['http_proxy'] = config.http_proxy
    os.environ['https_proxy'] = config.https_proxy
    os.environ['no_proxy'] = os.getenv('no_proxy') + ',' + config.no_proxy   