import logging
from typing import List
import requests
import threading
import time
import sqlite3
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # Без этого флага будут выводиться в консоль сообщения о несекьюрном запросе.

base_url = 'http://swapi.dev/api/people/'
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)


# # Создаём таблицу, если её нет
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS results (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT,
#     age TEXT,
#     gender TEXT
# )
# ''')
#
# conn.commit()


def get_data_and_load(url: str, counter: int):
    """
    Функция получает по API данные о персонаже star wars, далее сохраняет имя, год рождения и пол персонажа в БД.
    :param url: Адрес API
    :param counter: Счетчик, который определяет сколько персонажей скачиваем.
    :return: none
    """
    response = requests.get(url + str(counter), verify=False)
    response_as_json = response.json()
    name = response_as_json.get("name")
    age = response_as_json.get("birth_year")
    gender = response_as_json.get("gender")
    # logger.info(f'{name}, {age}, {gender}')
    with sqlite3.connect('api_results.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO results (name, age, gender) VALUES (?, ?, ?)', (name, age, gender))
        conn.commit()


def sequential_work(url: str, counter: int):
    """
    Данная фукнция обрабатывает запросы к API и БД последовательно.
    """
    start = time.time()
    for i in range(1, counter):
        get_data_and_load(url, counter)
    end = time.time()
    duration = end - start
    logger.info('Sequential - done in {:.4}'.format(duration))


def multithreading_work(url: str, counter: int) -> None:
    """
    Данная фукнция обрабатывает запросы к API и БД в многопоточном режиме.
    """
    start = time.time()
    threads: List[threading.Thread] = []
    for i in range(1, counter):
        thread = threading.Thread(target=get_data_and_load, args=(url, counter))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    end = time.time()
    duration = end - start
    logger.info('Multithreading done in {:.4}'.format(duration))


if __name__ == '__main__':
    sequential_work(base_url, 21)
    multithreading_work(base_url, 21)
