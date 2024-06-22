import httpx
from time import sleep
from random import randint, choice
from httpx_observer.transport import PrometheusTransport
from httpx_observer.metrics import ProcessingRequestsMetric, RequestsDurationMetric, TotalRequestsMetric
from prometheus_client import start_http_server
from concurrent.futures import ThreadPoolExecutor

metrics = [
    TotalRequestsMetric(),
    RequestsDurationMetric(),
    ProcessingRequestsMetric(),
]

class FakeTransport(httpx.BaseTransport):

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        sleep(randint(1, 3))
        return httpx.Response(choice([200, 400, 500]))

transport = PrometheusTransport(FakeTransport(), metrics=metrics)

client = httpx.Client(transport=transport)

start_http_server(8000)

executor = ThreadPoolExecutor(max_workers=100)

while True:

    for i in range(randint(1, 100)):
        executor.submit(client.get, "http://example.com")
    sleep(5)
