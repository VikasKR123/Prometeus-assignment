from flask import Flask, render_template
from prometheus_client import Counter, generate_latest, Summary, Gauge
import time
import psutil

app = Flask(__name__)

REQUEST_COUNT = Counter('flask_app_request_count', 'Total button clicks')
REQUEST_TIME = Summary('flask_app_request_processing_seconds', 'Time spent processing requests')
CPU_USAGE = Gauge('flask_app_cpu_usage', 'CPU Usage')
MEMORY_USAGE = Gauge('flask_app_memory_usage', 'Memory Usage')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/click')
@REQUEST_TIME.time()
def click():
    REQUEST_COUNT.inc()
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().percent)
    return 'Button clicked!'

@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
