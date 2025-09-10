import logging
from typing import List
import requests
import threading
import time
import sqlite3
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # Без этого флага будут выводиться в консоль сообщения о несекьюрном запросе.
from multiprocessing.pool import ThreadPool
import multiprocessing




base_url = ['http://swapi.dev/api/people/' + str(i) for i in range(1, 21)]
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


def get_data_and_load(url: str):
    """
    Функция получает по API данные о персонаже star wars, далее сохраняет имя, год рождения и пол персонажа в БД.
    :param url: Адрес API
    :return: словарь с полученными данными, для отладки.
    """
    response = requests.get(url, verify=False)
    response_as_json = response.json()
    name = response_as_json.get("name")
    age = response_as_json.get("birth_year")
    gender = response_as_json.get("gender")
    # logger.info(f'{name}, {age}, {gender}')
    with sqlite3.connect('api_results.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO results (name, age, gender) VALUES (?, ?, ?)', (name, age, gender))
        conn.commit()
    return {  # Возвращаем данные
        "name": name,
        "age": age,
        "gender": gender,
        "status": "success"
    }


def threadpool_work() -> None:
    """
    Данная фукнция обрабатывает запросы к API и БД в многопоточном режиме через ThreadPool.
    """
    pool = ThreadPool(processes=multiprocessing.cpu_count() * 5)
    start = time.time()
    result = pool.map(get_data_and_load, base_url)
    logger.info(f'result is - {result}')
    pool.close()
    pool.join()
    end = time.time()
    duration = end - start
    logger.info('Multithreading with ThreadPool done in {:.4}'.format(duration))


def pool_work() -> None:
    """
    Данная фукнция обрабатывает запросы к API и БД в многопоточном режиме через Pool.
    """
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    start = time.time()
    result = pool.map(get_data_and_load, base_url)
    logger.info(f'result is - {result}')
    pool.close()
    pool.join()
    end = time.time()
    duration = end - start
    logger.info('Multithreading with Pool done in {:.4}'.format(duration))


if __name__ == '__main__':
    pool_work()
    threadpool_work()
