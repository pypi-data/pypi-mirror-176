from urllib.parse import urljoin, urlencode
from urllib3.connection import HTTPConnection
import socket

import arivo
import requests


class HttpBackend:
    def __init__(self, timeout):
        self._session = requests.Session()
        self.timeout = timeout

        # enable tcp keepalive if not already enabled
        if not any([opt[0] == socket.SO_KEEPALIVE for opt in HTTPConnection.default_socket_options]):
            HTTPConnection.default_socket_options.append((socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1))

    def get_url(self, *args, **query_params):
        url = urljoin(arivo.api_url, "/".join(x.strip("/") for x in args)) + "/"
        if query_params:
            return f"{url}?{urlencode(query_params)}"
        else:
            return url

    def request(self, method, url_parts, body=None, query_params=None):
        query_params = query_params or {}
        url_parts = self.get_url(*url_parts, **query_params)
        if arivo.api_token:
            self._session.headers["Authorization"] = f"APIToken {arivo.api_token}"
        response = self._session.request(method, url_parts, json=body, timeout=self.timeout)
        response.raise_for_status()
        return response
