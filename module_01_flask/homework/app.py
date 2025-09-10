import datetime
import os
from datetime import timedelta
from flask import Flask
import random

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Текущая директория
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt') # Абсолютный путь к файлу
cars = ['Chevrolet', 'Renault', 'Ford', 'Lada'] # Список автомобилей
cats = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин'] #Список пород кошек
counter_of_visits = 0 #Глобальная переменная для подсчета количества посещений страницы


@app.route('/hello_world')
def return_hello_str() -> str:
    """
    Функция для вывода сообщения "Привет мир!"
    :return:
    string - строка с сообщением.
    """
    return f"Привет, Мир!"


@app.route('/cars')
def print_cars_list() -> str:
    """
    Функция формирует строку из списка моделей автомобилей.
    :return:
    string - строка с автомобилями.
    """
    result_string = f'Список машин: '
    list_length = len(cars)
    for i_car in cars:
        if i_car == cars[list_length - 1]:
            result_string += i_car + '.'
        else:
            result_string += i_car + ', '
    return result_string

@app.route('/cats')
def random_cat()-> str:
    """
    Функция формирует строку с одной из пород кошек из списка cats.
    :return:
    string - строка с одной случайной породой кошки.
    """
    random_cat = random.choice(cats)
    return f'Вам попалась кошка породы: {random_cat}'


@app.route('/get_time/now')
def print_current_time() -> str:
    """
    Функция формирует строку с текущим временем и датой
    :return:
    string - стркоа с текущим временем и датой
    """
    current_time = datetime.datetime.now()
    return f'Текущее время: {current_time}'

@app.route('/get_time/future')
def print_future_time() -> str:
    """
    Функция формирует строку с датой и временем, у которого к текущему значению часа прибавлена единица.
    :return:
    string - строка с датой и временем, у которого к текущему значению часа прибавлена единица.
    """
    hour = timedelta(hours=1)
    current_time = datetime.datetime.now()
    future_time = datetime.datetime.now() + hour
    return 'Текущее время: {}<br>Через 1 час будет: {}'.format(current_time, future_time)


def get_list_of_words(path_to_file:str) -> list:
    """
    Функция для получения списка из слов, считанных из файла.
    :param path_to_file: путь к файлу для обработки.
    :return:
    list - список слов из файла. Если файл не найден, то возвращется пустой список.
    """
    try:
        with open(path_to_file, 'r', encoding='utf-8') as file:
            text = file.read()
            # Удаляем знаки препинания и переводим в нижний регистр
            text = ''.join(e for e in text if e.isalnum() or e.isspace()).lower()
            words = text.split()
            return words
    except FileNotFoundError:
        print(f"Файл {path_to_file} не найден.")
        return []

words_from_war_and_peace = get_list_of_words(BOOK_FILE)

@app.route('/get_random_word')
def return_random_word() ->str:
    """
    Функция формирует строку с рандомным словом из списка слов.
    :return:
    string - строка с рандомным словом.
    """
    random_word = random.choice(words_from_war_and_peace)
    return f'Случаное слово из произведения "Война и мир: {random_word}"'


@app.route('/counter')
def print_counter()->str:
    """
    Функция для посчета количества посещений страницы.
    :return:
    string - строка с счетчиком.
    """
    global counter_of_visits
    counter_of_visits  += 1
    return f"Счетчик посещений этой страницы  равен: {counter_of_visits}"



if __name__ == '__main__':
    app.run(debug=True)
