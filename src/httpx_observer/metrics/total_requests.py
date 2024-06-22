import httpx
from prometheus_client import Counter
import typing as t

class TotalRequestsMetric(httpx.BaseTransport):
    def __init__(self, next_transport: t.Optional[httpx.BaseTransport] = None):
        self._http_client_requests_total = Counter(
            name="httpx_requests_total",
            documentation="HTTP Requests",
            labelnames=["method", "status_code", "endpoint"],
        )
        self._next_transport = next_transport

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        response = self._next_transport.handle_request(request)
        self._http_client_requests_total.labels(
            method=request.method,
            status_code=response.status_code,
            endpoint=request.url.path,
        ).inc()
        return response
