import random

from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

@app.route('/hello')
@metrics.counter(
    'hello_requests_total',
    'Total number of hello requests grouped by status code',
    labels = {'status': lambda resp: resp.status_code}
)
def hello_world():
    print("Hello endpoint called")
    if random.random() < 0.2:
        raise Exception("Эмулируем случайную ошибку!")
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)