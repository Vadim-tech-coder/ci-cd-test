import sqlite3

ENABLE_FOREIGN_KEY = "PRAGMA foreign_keys = ON;"

FILL_BOOKS_TABLE = """
INSERT INTO books
(name, count, release_date, author_id) VALUES (?, ?, ?, ?)"""
BOOKS_DATA = [('War and peace', 5, '1990-02-05', 1),
('World War 2', 3, '1945-02-05', 2),
('SVO(Z)', 5, '2025-02-06', 3)]

FILL_AUTHORS_TABLE = """
INSERT INTO authors
(name, surname) VALUES (?, ?)"""
AUTHORS_DATA = [('Лев', 'Толстой'),
('Иван', 'Иванов'),
('Петр', 'Ян')]


FILL_STUDENTS_TABLE = """
INSERT INTO students
(name, surname, phone, email, average_score, scholarship) VALUES (?, ?, ?, ?, ?, ?)"""
STUDENTS_DATA = [('Вадим', 'Левако', '79645558789', 'test@test.ru', 5, True),
('Сидор', 'Сидоров', '79645558788', 'test222@test.ru', 4, True),
('Анатолий', 'Силуянов', '79645558555', 'test333@test.ru', 3, False)]


FILL_RECEIVED_BOOKS_TABLE = """
INSERT INTO receiving_books
(book_id, student_id, date_of_issue, date_of_return) VALUES (?, ?, ?, ?)"""
RECEIVED_BOOKS_DATA = [(1, 1, '2025-01-05', '2025-01-30'),
(2, 2, '2025-02-05', '2025-02-20'),
(3, 3, '2025-03-05', '2025-03-30'),]


def fill_tables() -> None:
    with sqlite3.connect("library_new.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.executescript(ENABLE_FOREIGN_KEY)

        for author in AUTHORS_DATA:
            cursor.execute(FILL_AUTHORS_TABLE, author)

        for book in BOOKS_DATA:
            cursor.execute(FILL_BOOKS_TABLE, book)

        for student in STUDENTS_DATA:
            cursor.execute(FILL_STUDENTS_TABLE, student)

        for rec_book in RECEIVED_BOOKS_DATA:
            cursor.execute(FILL_RECEIVED_BOOKS_TABLE, rec_book)

if __name__ == '__main__':
    fill_tables()