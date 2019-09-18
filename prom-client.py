from flask import Response, Flask, request
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge
import random, time

# Create my app
app = Flask(__name__)

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
_INF = float("inf")

graphs = {}
graphs['c'] = Counter('test_of_counter', 'Description of counter')
graphs['h'] = Histogram('test_of_histogram', 'Description of histogram', buckets=(1, 5, 10, 50, 100, 200, 500, _INF))
graphs['g'] = Gauge('test_of_gauge', 'Description of gauge')

@app.route("/update/count", methods=["GET"])
def update_count():
    graphs['c'].inc()
    return requests_count()

@app.route("/update/histogram", methods=["GET"])
def update_histogram():
    print request.args
    k = float(request.args.get('value'))
    graphs['h'].observe(k)
    return requests_count()

@app.route("/update/gauge", methods=["GET"])
def update_gauge():
    print request.args
    k = request.args.get('value')
    graphs['g'].set(k)
    return requests_count()

@app.route("/metrics")
def requests_count():
    res = []
    for k,v in graphs.iteritems():
        res.append(prometheus_client.generate_latest(v))
    # res = [prometheus_client.generate_latest(c), prometheus_client.generate_latest(h), prometheus_client.generate_latest(g)]
    return Response(res, mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
