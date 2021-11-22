from flask import Flask, Response
from pgsql_exporter import Exporter

app = Flask(__name__)

@app.route("/metrics")
def metrics():
    e = Exporter()
    all_metrics = e.metrics()
    return Response(all_metrics, mimetype='text/plain')
    return all_metrics