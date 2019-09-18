from prometheus_client import start_http_server, Summary, Counter, Histogram, Gauge, MetricsHandler
import random
import time

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
_INF = float("inf")

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time."""
    c.inc()  # Increment by 1
    h.observe(t * 100)
    time.sleep(t)
    g.set(t)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)

    c = Counter('test_of_counter', 'Description of counter')
    h = Histogram('test_of_histogram', 'Description of histogram', buckets=(1, 5, 10, 50, 100, 200, 500, _INF))
    g = Gauge('test_of_gauge', 'Description of gauge')

    # Generate some requests.
    while True:
        process_request(random.random())
