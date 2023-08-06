import os
from typing import Any, Dict
import requests
import json
import logging
import time
import sys
import urllib3
from .utils import load_config
from .proxy import add_proxy
from .models import ConfigModel, ProxyModel, TargetAPI, RequestResponse


class ApiClient:
    def __init__(
        self, 
        config_file_path: str,
        proxy: ProxyModel = None,
        debug: bool =False,
        disable_ssl_warning=True,
        **kwargs
    ) -> None:
        self.logger = kwargs.get('logger') or logging.getLogger('ndd_rest_tools')
        self.debug = debug
        if self.debug:
            self.logger.addHandler(logging.StreamHandler(sys.stdout))
            self.logger.level = logging.DEBUG

        if disable_ssl_warning:
            self.logger.debug('disable InsecureRequestWarning')
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        if proxy:
            self.logger.info(f'add proxy {proxy}')
            add_proxy(proxy)
        self.config: ConfigModel = load_config(config_file_path)
        self.logger.debug(f'config file -> {self.config}')        

    def _make_url_for_get_method(self, url: str, params: Dict) -> str:
        url += '?'
        for k, v in params.items():
            url += f'{str(k)}={str(v)}&'
        if url.endswith('&'):
            url = url[0:-1]
        self.logger.debug(f'make url result -> {url}')
        return url

    def make_request(
        self, 
        target_name: str, 
        headers: Dict=None, 
        parameters: Dict=None
    ) -> RequestResponse:
        target: TargetAPI = self.config.config.get(target_name)
        if not target:
            self.logger.error(f'not config for api endpoint -> {target_name}')
            return RequestResponse(message=f"not config for api endpoint {target_name}")
        
        _url = target.url
        _method = target.method
        _headers = target.header
        _parameters = target.parameters

        # update params
        if headers:
            _headers.update(headers)
            self.logger.debug(f'change request header -> {_headers}')
        if parameters:
            _parameters.update(parameters)
            self.logger.debug(f'change parameters header -> {_parameters}')
        
        # handle url for method get
        if _method.lower() == 'get':
            _url = self._make_url_for_get_method(_url, _parameters)
            response = requests.get(_url, headers=_headers, verify=False)
        elif _method.lower() == 'post':
            _jdata = json.dumps(_parameters)
            self.logger.debug(f'request body {_jdata}')
            response = requests.post(_url, headers=_headers, verify=False, data=_jdata)
        else:
            raise ValueError('just support get and post')

        self.logger.debug(f'response object {response}')
        try:
            response_data = json.loads(response.text)
        except:
            response_data = None

        if 200 <= response.status_code <= 300:
            return RequestResponse(success=True, data=response_data, code=response.status_code)
        else:
            return RequestResponse(success=False, data=response_data, code=response.status_code)


