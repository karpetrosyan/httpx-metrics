import time

import httpx

from httpx_metrics.metrics_registry import HTTPX_CLIENT_REQUESTS_DURATION_SECONDS

from .base import BaseMetricTransport


class RequestsDurationMetric(BaseMetricTransport):
    def handle_request(self, request: httpx.Request) -> httpx.Response:
        t1 = time.monotonic()
        response = self.next_transport.handle_request(request)
        t2 = time.monotonic()
        HTTPX_CLIENT_REQUESTS_DURATION_SECONDS.labels(
            method=request.method,
            status_code=response.status_code,
            path=request.url.path,
            version=response.extensions["http_version"],
        ).observe(t2 - t1)

        return response
