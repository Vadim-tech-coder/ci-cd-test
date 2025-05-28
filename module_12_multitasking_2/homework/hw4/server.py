from datetime import datetime
import logging
import requests
from threading import Thread
import time
from flask import Flask


logging.basicConfig(filename='timestamp.log', filemode='w', encoding='utf8',
                    level=logging.INFO, format="%(threadName)s %(message)s")
logger = logging.getLogger(__name__)

base_url = 'http://127.0.0.1:8080/timestamp/'

def get_timestamp():
    for _ in range(20):
        current_timestamp = datetime.now().timestamp()
        response = requests.get(base_url + str(current_timestamp))
        if response.status_code == 200:
            logger.info(f"{current_timestamp} : {response.text}")
        time.sleep(1)

app: Flask = Flask(__name__)

@app.route('/timestamp/<timestamp>')
def timestamp_handler(timestamp: str) -> str:
    timestamp: float = float(timestamp)
    return str(datetime.fromtimestamp(timestamp))

def run_flask():
    app.run('127.0.0.1', port=8080, use_reloader=False)

if __name__ == '__main__':
    # app.run('127.0.0.1', port=8080)
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    start = time.time()
    threads = [Thread(target=get_timestamp) for _ in range(10)]
    for thread in threads:
        thread.start()
        time.sleep(1)

    for thread in threads:
        thread.join()
    end = time.time()
    duration = end - start
    logger.info(f'Конец основной программы, время выполнения - {duration}')