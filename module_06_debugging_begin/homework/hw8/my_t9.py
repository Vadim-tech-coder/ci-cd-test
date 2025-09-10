"""
У нас есть кнопочный телефон (например, знаменитая Nokia 3310), и мы хотим,
чтобы пользователь мог проще отправлять СМС. Реализуем своего собственного клавиатурного помощника.

Каждой цифре телефона соответствует набор букв:
* 2 — a, b, c;
* 3 — d, e, f;
* 4 — g, h, i;
* 5 — j, k, l;
* 6 — m, n, o;
* 7 — p, q, r, s;
* 8 — t, u, v;
* 9 — w, x, y, z.

Пользователь нажимает на клавиши, например 22736368, после чего на экране печатается basement.

Напишите функцию my_t9, которая принимает на вход строку, состоящую из цифр 2–9,
и возвращает список слов английского языка, которые можно получить из этой последовательности цифр.
"""
from typing import List
from collections import defaultdict

numbers_to_letters = {
    'a': '2', 'b': '2', 'c': '2',
    'd': '3', 'e': '3', 'f': '3',
    'g': '4', 'h': '4', 'i': '4',
    'j': '5', 'k': '5', 'l': '5',
    'm': '6', 'n': '6', 'o': '6',
    'p': '7', 'q': '7', 'r': '7', 's': '7',
    't': '8', 'u': '8', 'v': '8',
    'w': '9', 'x': '9', 'y': '9', 'z': '9'
}



def load_file(path:str):
    """
    Функция для загрузки информации из файла в массив
    :param path: путь к файлу
    :return: список слов, в нижнем регистре, без символов переноса строки.
    """
    with open(path, 'r', encoding='utf8') as file:
        file_data = file.readlines()
        file_data = [line.strip().lower() for line in file_data]
        return file_data


def word_to_digit(word):
    """
    Функция для преобразования слова в цифры в соответствии со словарем Т9.
    :param word: слово для преобразования
    :return: строка из чисел соответствующих введеному слову в Т9.
    """
    return ''.join(numbers_to_letters.get(char, '') for char in word.lower() if char.isalpha())


def my_t9(input_numbers: str) -> List[str]:
    """
    Функция принимает на вход пользовательский ввод из чисел,
    далее если слово удалось преобразовать в числовую последовательность Т9, добавляет в словарь.
    :param input_numbers: строка, состоящая из чисел.
    :return: часть словаря, которая является списком слов.
    """
    t9_index = defaultdict(list)
    for word in words_list:
        digits = word_to_digit(word)
        if digits:
            t9_index[digits].append(word)
    return t9_index[input_numbers]

if __name__ == '__main__':
    words_list = load_file('words.txt')
    numbers: str = input()
    words: List[str] = my_t9(numbers)
    print(*words, sep='\n')

