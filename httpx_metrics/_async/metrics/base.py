import typing as t

import httpx


class AsyncBaseMetricTransport(httpx.AsyncBaseTransport):
    def __init__(self) -> None:
        self._next_transport: t.Optional[httpx.AsyncBaseTransport] = None

    @property
    def next_transport(self) -> httpx.AsyncBaseTransport:
        assert self._next_transport, "next_transport is not set"
        return self._next_transport

    @next_transport.setter
    def next_transport(self, value: httpx.AsyncBaseTransport):
        self._next_transport = value
