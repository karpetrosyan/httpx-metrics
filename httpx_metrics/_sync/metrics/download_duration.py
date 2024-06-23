import time

import httpx

from httpx_metrics.metrics_registry import HTTPX_RESPONSE_DOWNLOAD_DURATION_SECONDS

from .base import BaseMetricTransport


class DownloadResponse(httpx.Response):
    def __init__(self, *args, **kwargs):
        self._path = kwargs.pop("path")
        self._method = kwargs.pop("method")
        self._version = kwargs["extensions"]["http_version"]

        super().__init__(*args, **kwargs)
        self._download_start = time.monotonic()

    def close(self) -> None:
        download_end = time.monotonic() - self._download_start

        HTTPX_RESPONSE_DOWNLOAD_DURATION_SECONDS.labels(
            method=self._method,
            status_code=self.status_code,
            path=self._path,
            version=self._version,
        ).observe(download_end)
        return super().close()


class DownloadDurationMetric(BaseMetricTransport):
    def handle_request(self, request: httpx.Request) -> httpx.Response:
        response = self.next_transport.handle_request(request)

        return DownloadResponse(
            status_code=response.status_code,
            headers=response.headers,
            stream=response.stream,
            extensions=response.extensions,
            path=request.url.path,
            method=request.method,
        )
