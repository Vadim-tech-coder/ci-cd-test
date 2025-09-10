"""
Удобно направлять результат выполнения команды напрямую в программу с помощью конвейера (pipe):

$ ls -l | python3 get_mean_size.py

Напишите функцию get_mean_size, которая на вход принимает результат выполнения команды ls -l,
а возвращает средний размер файла в каталоге.
"""

import sys


def get_mean_size(ls_output: str) -> float:

    """Функция для посчета среднего размера файла в директории.
    args:
        ls_output - результат выода команды ls с флагом -l
    returns:
        mean_size_of_file - срдний размер файла, который округляется до 2 символов после запятой."""

    mean_size_of_file = 0
    lines = ls_output.split('\n')
    lines_count = len(lines)
    for line in lines:
        if line.startswith('total') or line.startswith('d'):
            continue
        else:
            if line == '':
                lines_count -= 1
            else:
                mean_size_of_file += int(line.split()[5])
    mean_size_of_file = round(mean_size_of_file / lines_count, 2)
    return mean_size_of_file


if __name__ == '__main__':
    data: str = sys.stdin.read()
    mean_size: float = get_mean_size(data)
    print(mean_size)
