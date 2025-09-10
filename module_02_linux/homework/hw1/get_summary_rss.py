

"""
С помощью команды ps можно посмотреть список запущенных процессов.
С флагами aux эта команда выведет информацию обо всех процессах, запущенных в системе.

Запустите эту команду и сохраните выданный результат в файл:

$ ps aux > output_file.txt

Столбец RSS показывает информацию о потребляемой памяти в байтах.

Напишите функцию get_summary_rss, которая на вход принимает путь до файла с результатом выполнения команды ps aux,
а возвращает суммарный объём потребляемой памяти в человекочитаемом формате.
Это означает, что ответ надо перевести в байты, килобайты, мегабайты и так далее.
"""
import os

file_name= 'output_file.txt'
calculated_path = os.path.abspath(os.path.join(file_name))

def get_summary_rss(ps_output_file_path: str) -> str:
    with open(ps_output_file_path, 'r', encoding='utf8') as file:
        file_lines = file.readlines()
        total_memory_in_bytes = 0
        units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
        for line in file_lines:
            if line.startswith("USER"):
                continue
            else:
                total_memory_in_bytes += int(line.split()[5])
        for unit in units:
            if total_memory_in_bytes < 1024:
                return f"Суммарный объем памяти: {total_memory_in_bytes:.2f} {unit}"
            total_memory_in_bytes /= 1024


        return f"Суммарный объем памяти: {total_memory_in_bytes:.2f} YB"


if __name__ == '__main__':
    path: str = calculated_path
    summary_rss: str = get_summary_rss(path)
    print(summary_rss)
