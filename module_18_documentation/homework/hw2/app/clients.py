import json
import multiprocessing
import time
from multiprocessing.pool import ThreadPool

import requests

import logging

logging.basicConfig(level=logging.DEBUG)


class AuthorClient:
    URL: str = 'http://127.0.0.1:5000/api/authors'
    TIMEOUT: int = 1

    def __init__(self):
        self.session = requests.Session()

    def get_all_authors(self) -> dict:
        response = requests.get(self.URL, timeout=self.TIMEOUT)
        return response.json()

    def get_books_by_author_id(self, author_id: int) -> dict:
        response = self.session.get(self.URL + f'/{author_id}', timeout=self.TIMEOUT)
        return response.json()

    def delete_author(self, author_id: int) -> dict:
        response = self.session.delete(self.URL + f'/{author_id}', timeout=self.TIMEOUT)
        return response.json()

class BookClient:
    URL: str = 'http://127.0.0.1:5000/api/books'
    TIMEOUT: int = 5

    def __init__(self):
        self.session = requests.Session()

    def get_all_books(self) -> dict:
        response = self.session.get(self.URL, timeout=self.TIMEOUT)
        return response.json()


    def get_book(self, book_id: int) -> dict:
        response = self.session.get(self.URL + f'/{book_id}', timeout=self.TIMEOUT)
        return response.json()

    def delete_book(self, book_id: int) -> dict:
        response = self.session.delete(self.URL + f'/{book_id}', timeout=self.TIMEOUT)
        return response.json()

    def change_book(self, book_id: int, data: dict):
        response = self.session.patch(self.URL + f'/{book_id}', json=data, timeout=self.TIMEOUT)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError('Wrong params. Response message: {}'.format(response.json()))

    def add_new_book(self, data: dict):
        response = self.session.post(self.URL, json=data, timeout=self.TIMEOUT)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError('Wrong params. Response message: {}'.format(response.json()))


array_with_execution_duration = []

def start_stop_timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start
        array_with_execution_duration.append(execution_time)
        return result
    return wrapper

@start_stop_timer
def many_requests_by_counter_no_session(counter: int):
    for _ in range(counter):
        author_client.get_all_authors()

@start_stop_timer
def many_requests_by_counter_with_session(counter: int):
    for _ in range(counter):
        author_client.session.get(author_client.URL)

@start_stop_timer
def many_requests_with_threadpool_no_session(counter: int):
    pool = ThreadPool(processes=multiprocessing.cpu_count())
    def call_get_all_authors(_):
        return author_client.get_all_authors()

    pool.map(call_get_all_authors, range(counter))
    pool.close()
    pool.join()


@start_stop_timer
def many_requests_with_threadpool_with_session(counter: int):
    pool = ThreadPool(processes=multiprocessing.cpu_count())
    pool.map(author_client.session.get, [author_client.URL for _ in range(counter)])
    pool.close()
    pool.join()


if __name__ == '__main__':
    # client_book = BookClient()
    # client_book.session.post(
    #     client_book.URL,
    #     data=json.dumps({'title': 'QWERTY3', 'author_id': 2}),
    #     headers={'content-type': 'application/json'}
    # )
    # client_book.session.get(client_book.URL)
    author_client = AuthorClient()
    many_requests_by_counter_no_session(10)
    many_requests_by_counter_no_session(100)
    many_requests_by_counter_no_session(1000)

    many_requests_by_counter_with_session(10)
    many_requests_by_counter_with_session(100)
    many_requests_by_counter_with_session(1000)

    many_requests_with_threadpool_no_session(10)
    many_requests_with_threadpool_no_session(100)
    many_requests_with_threadpool_no_session(1000)

    many_requests_with_threadpool_with_session(10)
    many_requests_with_threadpool_with_session(100)
    many_requests_with_threadpool_with_session(1000)

    print("NO SESSION:")
    print("Время выполнения 10 запросов: {}".format(array_with_execution_duration[0]))
    print("Время выполнения 100 запросов: {}".format(array_with_execution_duration[1]))
    print("Время выполнения 1000 запросов: {}".format(array_with_execution_duration[2]))

    print("WITH SESSION:")
    print("Время выполнения 10 запросов: {}".format(array_with_execution_duration[3]))
    print("Время выполнения 100 запросов: {}".format(array_with_execution_duration[4]))
    print("Время выполнения 1000 запросов: {}".format(array_with_execution_duration[5]))

    print("NO SESSION WITH POOL:")
    print("Время выполнения 10 запросов: {}".format(array_with_execution_duration[6]))
    print("Время выполнения 100 запросов: {}".format(array_with_execution_duration[7]))
    print("Время выполнения 1000 запросов: {}".format(array_with_execution_duration[8]))

    print("WITH SESSION WITH POOL:")
    print("Время выполнения 10 запросов: {}".format(array_with_execution_duration[9]))
    print("Время выполнения 100 запросов: {}".format(array_with_execution_duration[10]))
    print("Время выполнения 1000 запросов: {}".format(array_with_execution_duration[11]))

