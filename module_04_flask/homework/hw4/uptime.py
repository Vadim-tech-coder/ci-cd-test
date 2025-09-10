"""
Напишите GET-эндпоинт /uptime, который в ответ на запрос будет выводить строку вида f"Current uptime is {UPTIME}",
где UPTIME — uptime системы (показатель того, как долго текущая система не перезагружалась).

Сделать это можно с помощью команды uptime.
"""
import subprocess

from flask import Flask

app = Flask(__name__)


@app.route("/uptime", methods=['GET'])
def uptime() -> str:
    current_uptime = subprocess.check_output('uptime -p', shell=True).decode()
    return f"Текущее время работы {current_uptime[3:]}"


if __name__ == '__main__':
    app.run(debug=True)
