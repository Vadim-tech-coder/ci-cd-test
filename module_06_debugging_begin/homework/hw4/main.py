"""
Ваш коллега, применив JsonAdapter из предыдущей задачи, сохранил логи работы его сайта за сутки
в файле skillbox_json_messages.log. Помогите ему собрать следующие данные:

1. Сколько было сообщений каждого уровня за сутки.
2. В какой час было больше всего логов.
3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
4. Сколько сообщений содержит слово dog.
5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
"""
import json
import shlex
from datetime import datetime
from typing import Dict
import subprocess
import re
from collections import Counter


def task1() -> Dict[str, int]:
    """
    1. Сколько было сообщений каждого уровня за сутки.
    @return: словарь вида {уровень: количество}
    """
    log_level_counters = {'INFO': 0, 'ERROR': 0, 'WARNING': 0, 'DEBUG': 0, 'CRITICAL': 0}
    for i_row in file_data:
        if i_row['level'] in log_level_counters.keys():
            log_level_counters[i_row['level']] += 1
    return log_level_counters


def task2() -> int:
    """
    2. В какой час было больше всего логов.
    @return: час
    """
    log_messages_per_each_hour = {}

    for i_row in file_data:
        i_row_as_date = datetime.strptime(i_row['time'], '%H:%M:%S').time().hour
        if log_messages_per_each_hour.get(i_row_as_date):
            log_messages_per_each_hour[i_row_as_date] += 1
        else:
            log_messages_per_each_hour[i_row_as_date] = 1

    hour_with_max_messages = max(log_messages_per_each_hour, key = log_messages_per_each_hour.get)
    return hour_with_max_messages

def safe_int(s):
    s = s.strip()
    if not s:
        return 0
    return int(s)


def task3() -> int:
    """
    3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
    @return: количество логов
    """
    command_line1 = """grep '"level": "CRITICAL"' skillbox_json_messages.log | grep '"time": "05:0[0-9]:' -c"""
    command_line2 = """grep '"level": "CRITICAL"' skillbox_json_messages.log | grep '"time": "05:1[0-9]:' -c"""
    command_line3 = """grep '"level": "CRITICAL"' skillbox_json_messages.log | grep '"time": "05:20-:' -c"""
    command_execution1 = subprocess.run(command_line1, capture_output=True, text=True, shell=True)
    command_execution2 = subprocess.run(command_line2, capture_output=True, text=True,  shell=True)
    command_execution3 = subprocess.run(command_line3, capture_output=True, text=True,  shell=True)
    try:
        result1 = safe_int(command_execution1.stdout.strip())
        result2 = safe_int(command_execution2.stdout.strip())
        result3 = safe_int(command_execution3.stdout.strip())
        result = result1 + result2 + result3
    except ValueError:
        pattern = r'\d+'
        result = (safe_int(re.search(pattern, command_execution1.stdout).group()) +
                  safe_int(re.search(pattern, command_execution2.stdout).group()) +
                  safe_int(re.search(pattern, command_execution3.stdout).group()))
    return result



def task4() -> int:
    """
    4. Сколько сообщений содержат слово dog.
    @return: количество сообщений
    """
    command_line = """grep -c 'dog' skillbox_json_messages.log"""
    command = shlex.split(command_line)
    command_execution = subprocess.run(command, capture_output=True, text=True)
    try:
        result = int(command_execution.stdout.strip())
    except ValueError:
        pattern = r'\d+'
        result = re.search(pattern, command_execution.stdout).group()
    return result


def task5() -> str:
    """
    5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
    @return: слово
    """
    log_messages_type_warning = []

    for i_row in file_data:
       if i_row['level'] == 'WARNING':
           for i_word in i_row['message'].split():
            log_messages_type_warning.append(i_word.lower())
    most_common_word = Counter(log_messages_type_warning).most_common(1)[0][0]
    return most_common_word


def load_file(path:str):
    data = []
    with open(path, 'r', encoding='utf8') as file:
        for line in file.readlines():
            data.append(json.loads(line))
        print(data)
        return data

if __name__ == '__main__':
    file_data = load_file('skillbox_json_messages.log')
    tasks = (task1, task2, task3, task4, task5)
    for i, task_fun in enumerate(tasks, 1):
        task_answer = task_fun()
        print(f'{i}. {task_answer}')
