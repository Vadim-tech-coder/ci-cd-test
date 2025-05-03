"""
1. Сконфигурируйте логгер программы из темы 4 так, чтобы он:

* писал логи в файл stderr.txt;
* не писал дату, но писал время в формате HH:MM:SS,
  где HH — часы, MM — минуты, SS — секунды с ведущими нулями.
  Например, 16:00:09;
* выводил логи уровня INFO и выше.

2. К нам пришли сотрудники отдела безопасности и сказали, что, согласно новым стандартам безопасности,
хорошим паролем считается такой пароль, который не содержит в себе слов английского языка,
так что нужно доработать программу из предыдущей задачи.

Напишите функцию is_strong_password, которая принимает на вход пароль в виде строки,
а возвращает булево значение, которое показывает, является ли пароль хорошим по новым стандартам безопасности.
"""

import getpass
import hashlib
import logging
from typing import List
import re

logger = logging.getLogger("password_checker")

words_file = "C:/Users/khambaleevvv/Downloads/words.txt"

def get_list_of_words_from_file(path:str) -> set:
    set_of_words = set()
    with open(path, 'r', encoding='utf8') as file:
        for i_line in file.readlines():
            if i_line.endswith('\n'):
                clear_line = i_line[:-2]
                if len(clear_line) > 4:
                    set_of_words.add(clear_line)
    return set_of_words


def is_strong_password(password: str, set_of_words: set) -> bool:
    password_lower_register = password.lower()
    pattern = r'[a-zA-Z]+'
    words_in_password = re.findall(pattern, password_lower_register)
    for i_word in words_in_password:
        if i_word in set_of_words:
            logger.info(f"Слово {i_word} БЫЛО найдено в словаре.")
            return False
    logger.info(f"Слова {words_in_password} не найдено|ы в словаре.")
    return True


def input_and_check_password() -> bool:
    logger.debug("Начало input_and_check_password")
    password: str = getpass.getpass()

    if not password:
        logger.warning("Вы ввели пустой пароль.")
        return False
    elif not is_strong_password(password, set_of_words=words_set):
        logger.warning("Вы ввели слишком слабый пароль!")
        return False
    logger.warning("Пароль соответствует требованиям безопасности!")

    try:
        hasher = hashlib.md5()

        hasher.update(password.encode("latin-1"))

        if hasher.hexdigest() == "098f6bcd4621d373cade4e832627b4f6":
            return True
    except ValueError as ex:
        logger.exception("Вы ввели некорректный символ ", exc_info=ex)

    return False


if __name__ == "__main__":
    words_set = get_list_of_words_from_file(words_file)
    FORMAT = '%(asctime)s %(name)s %(levelname)s %(message)s'
    custom_time_format = "%H:%M:%S"
    logging.basicConfig(level=logging.INFO, filename="stderr.txt",
                        encoding='utf8', format=FORMAT, datefmt=custom_time_format)
    logger.info("Вы пытаетесь аутентифицироваться в Skillbox")
    count_number: int = 3
    logger.info(f"У вас есть {count_number} попыток")

    while count_number > 0:
        if input_and_check_password():
            exit(0)
        count_number -= 1

    logger.error("Пользователь трижды ввёл не правильный пароль!")
    exit(1)
