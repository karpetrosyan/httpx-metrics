import httpx

from httpx_metrics.metrics_registry import HTTPX_CLIENT_PROCESSING_REQUESTS

from .base import AsyncBaseMetricTransport


class AsyncProcessingRequestsMetric(AsyncBaseMetricTransport):
    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        HTTPX_CLIENT_PROCESSING_REQUESTS.labels(
            method=request.method,
            path=request.url.path,
        ).inc()
        try:
            response = await self.next_transport.handle_async_request(request)
        finally:
            HTTPX_CLIENT_PROCESSING_REQUESTS.labels(
                method=request.method,
                path=request.url.path,
            ).dec()
        return response
