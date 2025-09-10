import datetime
import sqlite3

sql_for_logging = """
INSERT INTO birds 
(name, count, time) VALUES (?, ?, ?)
"""

def log_bird(
        cursor_log: sqlite3.Cursor,
        bird_name: str,
        date_time: str,
) -> None:
    data = (bird_name, count, date_time)
    cursor_log.execute(sql_for_logging, data)


sql_request_already_exist = """
SELECT EXISTS (
SELECT * FROM birds WHERE name = ?
);
"""

def check_if_such_bird_already_seen(
        cursor_check: sqlite3.Cursor,
        bird_name: str
) -> bool:
    response = cursor_check.execute(sql_request_already_exist, (bird_name, ))
    result = response.fetchone()[0]
    # print(result)
    return result


sql_for_table_creation = """
CREATE TABLE IF NOT EXISTS birds (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
count INTEGER NOT NULL, time VARCHAR NOT NULL)
"""

if __name__ == "__main__":
    print("Программа помощи ЮНатам v0.1")
    name: str = input("Пожалуйста введите имя птицы\n> ")
    count_str: str = input("Сколько птиц вы увидели?\n> ")
    count: int = int(count_str)
    right_now: str = datetime.datetime.utcnow().isoformat()

    with sqlite3.connect("../homework.db") as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute(sql_for_table_creation)

        if check_if_such_bird_already_seen(cursor, name):
            print("Такую птицу мы уже наблюдали!")

        log_bird(cursor, name, right_now)