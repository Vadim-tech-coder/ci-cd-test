"""
Каждый лог содержит в себе метку времени, а значит, правильно организовав логирование,
можно отследить, сколько времени выполняется функция.

Программа, которую вы видите, по умолчанию пишет логи в stdout. Внутри неё есть функция measure_me,
в начале и в конце которой пишется "Enter measure_me" и "Leave measure_me".
Сконфигурируйте логгер, запустите программу, соберите логи и посчитайте среднее время выполнения функции measure_me.
"""
import json
import logging
import random
from datetime import datetime, timedelta
from typing import List

logger = logging.getLogger(__name__)


def get_data_line(sz: int) -> List[int]:
    try:
        logger.debug("Enter get_data_line")
        return [random.randint(-(2 ** 31), 2 ** 31 - 1) for _ in range(sz)]
    finally:
        logger.debug("Leave get_data_line")


def measure_me(nums: List[int]) -> List[List[int]]:
    logger.debug("Enter measure_me")
    results = []
    nums.sort()

    for i in range(len(nums) - 2):
        logger.debug(f"Iteration {i}")
        left = i + 1
        right = len(nums) - 1
        target = 0 - nums[i]
        if i == 0 or nums[i] != nums[i - 1]:
            while left < right:
                s = nums[left] + nums[right]
                if s == target:
                    logger.debug(f"Found {target}")
                    results.append([nums[i], nums[left], nums[right]])
                    logger.debug(
                        f"Appended {[nums[i], nums[left], nums[right]]} to result"
                    )
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif s < target:
                    logger.debug(f"Increment left (left, right) = {left, right}")
                    left += 1
                else:
                    logger.debug(f"Decrement right (left, right) = {left, right}")

                    right -= 1

    logger.debug("Leave measure_me")

    return results


def load_file(path:str):
    """
    Функция для загрузки информации из файла логов.
    :param path: путь к файлу с логами
    :return: List - отфильтрованный список нужных строк из логов.
    """
    data_lines = []

    with open(path, 'r', encoding='utf8') as file:
        for line in file.readlines():
            parsed_line = json.loads(line)
            if parsed_line['MESSAGE'] == "Enter measure_me" or parsed_line['MESSAGE'] == "Leave measure_me":
                data_lines.append(parsed_line)
    return data_lines

def calculate_average(data_lines: List):
    """
    Функция для расчета среднего времени выполнения функции на основании массива, полученного из логов
    выполнения функции.
    :param data_lines: - отфильтрованный список нужных строк из логов.
    :return: среднее время выполнения функции.
    """
    data_durations = []
    index = 0
    while index < len(data_lines) - 1:
        start = data_lines[index]['time']
        end = data_lines[index + 1]['time']
        start_time = datetime.strptime(start, "%Y-%m-%d %H:%M:%S,%f")
        end_time = datetime.strptime(end, "%Y-%m-%d %H:%M:%S,%f")
        interval = end_time - start_time
        data_durations.append(interval)
        index += 2
    summa = sum(data_durations, timedelta())
    average = summa / len(data_durations)
    print(average)
    return average


if __name__ == "__main__":
    FORMAT = '{"time": "%(asctime)s", "LEVEL": "%(levelname)s", "MESSAGE": "%(message)s"}'
    logging.basicConfig(level="DEBUG", filename='measuring_logs.log', encoding='utf8', format=FORMAT)
    for it in range(15):
        data_line = get_data_line(10 ** 3)
        measure_me(data_line)
    list_to_process = load_file('measuring_logs.log')
    calculate_average(list_to_process)