import sqlite3


select_manager_salary = """
SELECT salary
FROM table_effective_manager
WHERE name = 'Иван Совин'
"""

select_worker_salary = """
SELECT salary
FROM table_effective_manager
WHERE name = ?
"""

update_worker_salary = """
UPDATE table_effective_manager
SET salary = ?
WHERE name = ?
"""

delete_worker = """
DELETE FROM table_effective_manager
WHERE name = ?"""

def ivan_sovin_the_most_effective(
        cursor: sqlite3.Cursor,
        name: str,
) -> None:
    result_manager = cursor.execute(select_manager_salary)
    manager_salary = result_manager.fetchone()[0]
    result_worker = cursor.execute(select_worker_salary, (name, ))
    result_worker_1 = result_worker.fetchone()
    if result_worker_1 is None:
        print(f"Не найдено сотрудника с именем {name}!")
    else:
        worker_salary =  result_worker_1[0]
        new_salary = worker_salary + worker_salary * 0.1
        if new_salary > manager_salary:
            cursor.execute(delete_worker, (name,))
            print(f'Сотрудник {name} уволен!')
        else:
            cursor.execute(update_worker_salary, (new_salary, name))
            print(f'Сотруднику {name} увеличена зарплата до {new_salary}!')

if __name__ == '__main__':
    name: str = input('Введите имя сотрудника: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        ivan_sovin_the_most_effective(cursor, name)
        conn.commit()
