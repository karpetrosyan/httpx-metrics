import typing as t

import httpx


class BaseMetricTransport(httpx.BaseTransport):
    def __init__(self) -> None:
        self._next_transport: t.Optional[httpx.BaseTransport] = None

    @property
    def next_transport(self) -> httpx.BaseTransport:
        assert self._next_transport, "next_transport is not set"
        return self._next_transport

    @next_transport.setter
    def next_transport(self, value: httpx.BaseTransport):
        self._next_transport = value
