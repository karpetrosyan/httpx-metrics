import httpx

from httpx_metrics.metrics_registry import HTTPX_CACHED_REQUESTS_TOTAL

from .base import BaseMetricTransport

try:
    import hishel
except ImportError:
    hishel = None  # type: ignore


class CachedRequestsMetric(BaseMetricTransport):
    def __init__(self) -> None:
        super().__init__()

        if hishel is None:
            raise RuntimeError(
                f"The `{type(self).__name__}` was used, "
                "but the required packages were not found. "
                "Check that you have `httpx-metrics` "
                "installed with the `hishel` extension as shown.\n"
                "```pip install httpx-metrics[hishel]```"
            )

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        response = self.next_transport.handle_request(request)

        if response.extensions.get("from_cache", None):
            HTTPX_CACHED_REQUESTS_TOTAL.labels(
                method=request.method,
                status_code=response.status_code,
                path=request.url.path,
                version=response.extensions["http_version"],
                revalidated=response.extensions["revalidated"],
            ).inc()

        return response
