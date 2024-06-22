import time

import httpx
from prometheus_client import Counter, Gauge, Histogram
import typing as t


class RequestsDurationMetric(httpx.BaseTransport):
    def __init__(self, next_transport: t.Optional[httpx.BaseTransport] = None):
        self._next_transport = next_transport
        self._http_client_requests_duration_seconds = Histogram(
            name="httpx_requests_duration_seconds",
            documentation="HTTP Requests duration",
            labelnames=["method", "endpoint"],
            buckets=[0.1, 0.3, 1, 1.5, 2, 3, 5, 10],
        )

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        t1 = time.monotonic()
        response = self._next_transport.handle_request(request)
        t2 = time.monotonic()
        self._http_client_requests_duration_seconds.labels(
            method=request.method, endpoint=request.url.path
        ).observe(t2 - t1)

        return response
