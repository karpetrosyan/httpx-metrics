import httpx

from httpx_metrics.metrics_registry import HTTPX_CLIENT_REQUESTS_TOTAL

from .base import AsyncBaseMetricTransport


class AsyncTotalRequestsMetric(AsyncBaseMetricTransport):
    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        response = await self.next_transport.handle_async_request(request)
        HTTPX_CLIENT_REQUESTS_TOTAL.labels(
            method=request.method,
            status_code=response.status_code,
            path=request.url.path,
            version=response.extensions["http_version"],
        ).inc()
        return response
