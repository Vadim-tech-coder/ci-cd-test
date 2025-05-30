import sqlite3


sql_request = """
SELECT EXISTS(
SELECT 1, 
SUM(CASE WHEN temperature_in_celsius < 16 OR temperature_in_celsius > 20 THEN 1 ELSE 0 END)
AS violations
FROM table_truck_with_vaccine
WHERE truck_number = ?
GROUP BY truck_number
HAVING
SUM(CASE WHEN temperature_in_celsius < 16 OR temperature_in_celsius > 20 THEN 1 ELSE 0 END) > 3
);
"""


def check_if_vaccine_has_spoiled(
        cursor: sqlite3.Cursor,
        truck_number: str
) -> bool:
    cursor.execute(sql_request, (truck_number, ))
    result = cursor.fetchone()
    # print(result)
    return result[0]

if __name__ == '__main__':
    truck_number: str = input('Введите номер грузовика: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        spoiled: bool = check_if_vaccine_has_spoiled(cursor, truck_number)
        print('Испортилась' if spoiled else 'Не испортилась')
        conn.commit()
