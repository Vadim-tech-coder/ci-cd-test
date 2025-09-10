import sqlite3
import csv

sql_request_to_delete = """
DELETE FROM table_fees 
WHERE truck_number = ? 
AND timestamp = ?
"""

def delete_wrong_fees(
        cursor: sqlite3.Cursor,
        wrong_fees_file: str
) -> None:
    with open(wrong_fees_file, newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            cursor.execute(sql_request_to_delete, (row['car_number'], row['timestamp']))
            # print(row['car_number'], row['timestamp'])


if __name__ == "__main__":
    with sqlite3.connect("../homework.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        delete_wrong_fees(cursor, "../wrong_fees.csv")
        conn.commit()
