import httpx

from httpx_metrics.metrics_registry import HTTPX_CLIENT_PROCESSING_REQUESTS

from .base import BaseMetricTransport


class ProcessingRequestsMetric(BaseMetricTransport):
    def handle_request(self, request: httpx.Request) -> httpx.Response:
        HTTPX_CLIENT_PROCESSING_REQUESTS.labels(
            method=request.method,
            path=request.url.path,
        ).inc()
        try:
            response = self.next_transport.handle_request(request)
        finally:
            HTTPX_CLIENT_PROCESSING_REQUESTS.labels(
                method=request.method,
                path=request.url.path,
            ).dec()
        return response
