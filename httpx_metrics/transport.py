import typing as t

import httpx
from prometheus_client import start_http_server

from httpx_metrics._async.metrics.base import AsyncBaseMetricTransport
from httpx_metrics._sync.metrics.base import BaseMetricTransport


class PrometheusTransport(httpx.BaseTransport):
    def __init__(
        self,
        next_transport: httpx.BaseTransport,
        metrics: t.Optional[t.List[BaseMetricTransport]] = None,
        exporter_port: t.Optional[int] = 8000,
    ):
        self._next_transport = next_transport

        for metric in (metrics or [])[::-1]:
            metric._next_transport = self._next_transport
            self._next_transport = metric

        if exporter_port is not None:
            start_http_server(exporter_port)

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        return self._next_transport.handle_request(request)


class AsyncPrometheusTransport(httpx.AsyncBaseTransport):
    def __init__(
        self,
        next_transport: httpx.AsyncBaseTransport,
        metrics: t.Optional[t.List[AsyncBaseMetricTransport]] = None,
        exporter_port: t.Optional[int] = 8000,
    ):
        self._next_transport = next_transport

        for metric in (metrics or [])[::-1]:
            metric._next_transport = self._next_transport
            self._next_transport = metric

        if exporter_port is not None:
            start_http_server(exporter_port)

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        return await self._next_transport.handle_async_request(request)
