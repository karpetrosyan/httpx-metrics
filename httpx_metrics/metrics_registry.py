from prometheus_client import Counter, Gauge, Histogram

# AsyncCachedRequestsMetric / CachedRequestsMetric

HTTPX_CACHED_REQUESTS_TOTAL = Counter(
    name="httpx_cached_requests_total",
    documentation="Cached HTTP Requests",
    labelnames=["method", "status_code", "path", "version", "revalidated"],
)

# AsyncDownloadDurationMetric / DownloadDurationMetric

HTTPX_RESPONSE_DOWNLOAD_DURATION_SECONDS = Histogram(
    name="httpx_response_download_duration_seconds",
    documentation="HTTP Response download duration",
    labelnames=["method", "status_code", "path", "version"],
    buckets=[
        0.001,  # 1 ms
        0.005,  # 5 ms
        0.01,  # 10 ms
        0.025,  # 25 ms
        0.05,  # 50 ms
        0.1,  # 100 ms
        0.25,  # 250 ms
        0.5,  # 500 ms
        1.0,  # 1 second
        2.5,  # 2.5 seconds
        5.0,  # 5 seconds
        10.0,  # 10 seconds
    ],
)

# AsyncProcessingRequestsMetric / ProcessingRequestsMetric

HTTPX_CLIENT_PROCESSING_REQUESTS = Gauge(
    name="httpx_processing_requests",
    documentation="HTTP Requests in progress",
    labelnames=["method", "path"],
)

# AsyncRequestsDurationMetric / RequestsDurationMetric

HTTPX_CLIENT_REQUESTS_DURATION_SECONDS = Histogram(
    name="httpx_requests_duration_seconds",
    documentation="HTTP Requests duration",
    labelnames=["method", "status_code", "path", "version"],
    buckets=[
        0.001,  # 1 ms
        0.005,  # 5 ms
        0.01,  # 10 ms
        0.025,  # 25 ms
        0.05,  # 50 ms
        0.1,  # 100 ms
        0.25,  # 250 ms
        0.5,  # 500 ms
        1.0,  # 1 second
        2.5,  # 2.5 seconds
        5.0,  # 5 seconds
        10.0,  # 10 seconds
    ],
)

# AsyncTotalRequestsMetric / TotalRequestsMetric

HTTPX_CLIENT_REQUESTS_TOTAL = Counter(
    name="httpx_requests_total",
    documentation="HTTP Requests",
    labelnames=["method", "status_code", "path", "version"],
)
