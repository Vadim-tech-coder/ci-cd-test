import sqlite3
import datetime
import random


WEEK = [(0, 'футбол'), (1, 'хоккей'), (2, 'шахматы'),
        (3, 'SUP серфинг'), (4, 'бокс'), (5, 'Dota 2'), (6, 'шах-бокс')]

sql_select = """
SELECT employee_id, date
FROM table_friendship_schedule
"""

def get_schedule():
    days = cursor.execute(sql_select).fetchall()
    days_week = []
    for date in days:
        day = datetime.datetime.strptime(date[1], '%Y-%m-%d')
        days_week.append((day.weekday(), date[0], date[1]))
    return days_week

sql_data_select = """
SELECT * FROM table_friendship_employees
"""


def get_employees_data():
    data = cursor.execute(sql_data_select).fetchall()
    return data


def get_new_schedule(schedule, employees):
    new_schedule = []
    for day_emp_date in schedule:
        id_emp = day_emp_date[1]
        day_of_week = day_emp_date[0]
        if WEEK[day_of_week][1] == employees[id_emp - 1][2]:
            while True:
                new_worker = random.choice(employees)
                if WEEK[day_of_week][1] != new_worker[2]:
                    new_schedule.append((new_worker[0], day_emp_date[2]))
                    break
        else:
            new_schedule.append((id_emp, day_emp_date[2]))
    return new_schedule


def update_work_schedule(cursor: sqlite3.Cursor) -> None:
    schedule = get_schedule()
    employees = get_employees_data()
    new_schedule = get_new_schedule(schedule, employees)
    cursor.execute("DELETE FROM table_friendship_schedule")
    cursor.executemany("INSERT INTO table_friendship_schedule (employee_id, date) VALUES (?, ?)", new_schedule)

if __name__ == '__main__':
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        update_work_schedule(cursor)
        conn.commit()
