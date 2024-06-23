import httpx
import pytest

from httpx_metrics import PrometheusTransport
from httpx_metrics._async.metrics.total_requests import AsyncTotalRequestsMetric
from httpx_metrics.sync_metrics import TotalRequestsMetric
from httpx_metrics.transport import AsyncPrometheusTransport


@pytest.mark.anyio
async def test_async_prometheus_transport():
    async_transport = AsyncPrometheusTransport(
        next_transport=httpx.MockTransport(
            handler=lambda request: httpx.Response(
                200, extensions={"http_version": b"HTTP/1.1"}
            )
        ),
        metrics=[AsyncTotalRequestsMetric()],
        exporter_port=None,
    )

    async with httpx.AsyncClient(transport=async_transport) as async_client:
        response = await async_client.get("https://example.com")
        assert response.status_code == 200


@pytest.mark.anyio
async def test_sync_prometheus_transport():
    sync_transport = PrometheusTransport(
        next_transport=httpx.MockTransport(
            handler=lambda request: httpx.Response(
                200, extensions={"http_version": b"HTTP/1.1"}
            )
        ),
        metrics=[TotalRequestsMetric()],
        exporter_port=None,
    )
    with httpx.Client(transport=sync_transport) as sync_client:
        response = sync_client.get("https://example.com")
        assert response.status_code == 200
