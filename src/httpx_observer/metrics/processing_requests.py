import time

import httpx
import typing as t
from prometheus_client import Counter, Gauge, Histogram


class ProcessingRequestsMetric(httpx.BaseTransport):
    def __init__(self, next_transport: t.Optional[httpx.BaseTransport] = None):
        self._next_transport = next_transport

        self._http_client_processing_requests = Gauge(
            name="httpx_processing_requests",
            documentation="HTTP Requests in progress",
            labelnames=["method", "endpoint"],
        )

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        self._http_client_processing_requests.labels(
            method=request.method, endpoint=request.url.path
        ).inc()
        try:
            response = self._next_transport.handle_request(request)
        finally:
            self._http_client_processing_requests.labels(
                method=request.method, endpoint=request.url.path
            ).dec()
        return response
