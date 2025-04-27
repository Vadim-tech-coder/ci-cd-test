"""
Консольная утилита lsof (List Open Files) выводит информацию о том, какие файлы используют какие-либо процессы.
Эта команда может рассказать много интересного, так как в Unix-подобных системах всё является файлом.

Но нам пока нужна лишь одна из её возможностей.
Запуск lsof -i :port выдаст список процессов, занимающих введённый порт.
Например, lsof -i :5000.

Как мы с вами выяснили, наш сервер отказывается запускаться, если кто-то занял его порт. Напишите функцию,
которая на вход принимает порт и запускает по нему сервер. Если порт будет занят,
она должна найти процесс по этому порту, завершить его и попытаться запустить сервер ещё раз.
"""
import shlex
import signal
import subprocess
from typing import List
import os
from flask import Flask

app = Flask(__name__)


def get_pids(port: int) -> List[int]:
    """
    Возвращает список PID процессов, занимающих переданный порт
    @param port: порт
    @return: список PID процессов, занимающих порт
    """
    command_line=f"lsof -i:{port}"

    if not isinstance(port, int):
        raise ValueError

    pids: List[int] = []
    command_result = subprocess.run(command_line, shell=True, capture_output=True, text=True)
    result_as_array = shlex.split(command_result.stdout)
    index = 10
    while index < len(result_as_array):
        pids.append(int(result_as_array[index]))
        index += 9
    return pids


def free_port(port: int) -> None:
    """
    Завершает процессы, занимающие переданный порт
    @param port: порт
    """
    pids: List[int] = get_pids(port)
    for i_process in pids:
        try:
            os.kill(i_process, signal.SIGKILL)
            print("Завершен процесс с PID: {}".format(i_process))
        except Exception as err_desc:
            print("Непредвиденные ошибки: {}".format(err_desc))

def run(port: int) -> None:
    """
    Запускает flask-приложение по переданному порту.
    Если порт занят каким-либо процессом, завершает его.
    @param port: порт
    """
    free_port(port)
    app.run(port=port)


if __name__ == '__main__':
    run(5000)
