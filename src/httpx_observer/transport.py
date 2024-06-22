import time

import httpx
from prometheus_client import Counter, Gauge, Histogram
import typing as t


class PrometheusTransport(httpx.BaseTransport):
    def __init__(self, next_transport: httpx.HTTPTransport, metrics: t.Optional[list[httpx.BaseTransport]] = None):
        self._next_transport = next_transport

        for metric in metrics[::-1] or []:
            metric._next_transport = self._next_transport
            self._next_transport = metric

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        return self._next_transport.handle_request(request)
