# httpx-metrics

httpx-metrics is a utility library that offers classes for integrating metrics into your httpx client (currently, it supports only Prometheus metrics).

[![PyPI - Version](https://img.shields.io/pypi/v/httpx-observer.svg)](https://pypi.org/project/httpx-observer)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/httpx-observer.svg)](https://pypi.org/project/httpx-observer)

-----

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Supported metrics](#supported-metrics)

## Installation

```console
pip install httpx-metrics
```

## Usage

```python
import httpx
import anyio
from httpx_metrics.async_metrics import (
    AsyncDownloadDurationMetric,
    AsyncProcessingRequestsMetric,
    AsyncRequestsDurationMetric,
    AsyncTotalRequestsMetric,
)
from httpx_metrics import AsyncPrometheusTransport

metrics_transport = AsyncPrometheusTransport(
    next_transport=httpx.AsyncHTTPTransport(),
    metrics=[
        AsyncRequestsDurationMetric(),
        AsyncTotalRequestsMetric(),
        AsyncProcessingRequestsMetric(),
        AsyncDownloadDurationMetric(),
    ],
    exporter_port=8000,
)


async def main():
    async with httpx.AsyncClient(transport=metrics_transport) as client:
        while True:
            response = await client.get("https://www.encode.io")
            await anyio.sleep(5)


anyio.run(main)
```

## Supported metrics

- **AsyncTotalRequestsMetric** / **TotalRequestsMetric**
    
    **Type**: Counter

    **Description**: Total number of requests

    **Labels**
    
    - method
    - status_code
    - path
    - version

- **AsyncRequestsDurationMetric** / **RequestsDurationMetric**

    **Type**: Histogram

    **Description**: Request duration in seconds

    **Labels**

    - method
    - status_code
    - path
    - version

- **AsyncProcessingRequestsMetric** / **ProcessingRequestsMetric**

    **Type**: Gauge

    **Description**: Number of requests in fly

    **Labels**

    - method
    - path

- **AsyncDownloadDurationMetric** / **DownloadDurationMetric**

    **Type**: Histogram

    **Description**: Response body downloading duration in seconds

    **Labels**

    - method
    - status_code
    - path
    - version

- **AsyncCachedRequestsMetric** / **CachedRequestsMetric**

    **Note**: This metric should be used on top of [hishel](hishel.com) transports

    **Type**: Counter

    **Description**: Total number of cached requests

    **Labels**

    - method
    - status_code
    - path
    - version
    - revalidated