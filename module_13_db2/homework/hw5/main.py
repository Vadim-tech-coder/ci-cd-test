import sqlite3
import random


sql_insert = """
INSERT INTO uefa_commands 
(command_number, command_name, command_country, command_level)
VALUES (?, ?, ?, ?)
"""

sql_check_not_empty = """
SELECT * FROM uefa_commands
"""

select_by_level = """
SELECT command_number 
FROM uefa_commands
WHERE command_level = ?"""


command_countries = ['Россия', 'Германия', 'Испания', 'Азербайджан', 'Англия', 'Иран', 'Словакия', 'Чехия', 'Нидерланды']
command_levels = ['Сильная', 'Слабая', 'Средняя']

def generate_test_data(
        cursor: sqlite3.Cursor,
        number_of_groups: int
) -> None:
    check_table = cursor.execute(sql_check_not_empty)
    rows = check_table.fetchall()
    if not rows:
        command_names = ["Команда №" + str(i + 1) for i in range(number_of_groups * 4 * 20)]
        number_of_team = 1
        for i_team in command_names:
            cursor.execute(sql_insert, (number_of_team, i_team,
                                        random.choice(command_countries),
                                        random.choice(command_levels)))
            number_of_team += 1
    for i_group in range(1, number_of_groups + 1):
        groups = []
        for i_level in command_levels:
            response = cursor.execute(select_by_level, (i_level,))
            command_number = response.fetchall()
            if i_level == 'Средняя':
                new_tuple = (i_group, )
                new_tuple += random.choice(command_number)
                groups.append(new_tuple)
            new_tuple = (i_group,)
            new_tuple += random.choice(command_number)
            groups.append(new_tuple)
        cursor.executemany("""INSERT INTO uefa_draw (group_number, command_number) VALUES (?, ?)""", groups)


if __name__ == '__main__':
    number_of_groups: int = int(input('Введите количество групп (от 4 до 16): '))
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        generate_test_data(cursor, number_of_groups)
        conn.commit()
