import sqlite3
from dataclasses import dataclass
from typing import Optional, Union, List, Dict

DATA = [
    {'id': 0, 'title': 'A Byte of Python', 'author_id': 1},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author_id': 2},
    {'id': 3, 'title': 'War and Peace', 'author_id': 3}
]

DATA_AUTHORS = [
    {'id': 1, 'first_name':'C.', 'last_name': 'Swaroop', 'middle_name': 'H.'},
    {'id': 2, 'first_name':'Herman', 'last_name': 'Melville'},
    {'id': 3, 'first_name':'Leo', 'last_name': 'Tolstoy'}
]

DATABASE_NAME = 'table_books.db'
BOOKS_TABLE_NAME = 'books'
AUTHORS_TABLE_NAME = 'authors'

@dataclass
class Book:
    title: str
    author_id: int
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


@dataclass
class Author:
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


def init_db(initial_records: List[Dict], initial_records_of_authors: List[Dict]) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")  # Включаем поддержку внешних ключей

        # Создаём таблицу authors, если её нет(как окаалось нужно сначал создавать дочернюю таблицу с внешним ключом, а потом родительскую)
        cursor.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{AUTHORS_TABLE_NAME}';"
        )
        exists_authors = cursor.fetchone()
        if not exists_authors:
            cursor.executescript(
                f"""
                CREATE TABLE `{AUTHORS_TABLE_NAME}`(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    first_name TEXT,
                    last_name TEXT, 
                    middle_name TEXT
                );
                """
            )
            cursor.executemany(
                f"""
                INSERT INTO `{AUTHORS_TABLE_NAME}`
                (id, first_name, last_name, middle_name) VALUES (?, ?, ?, ?)
                """,
                [
                    (item['id'], item['first_name'], item['last_name'], item.get('middle_name'))
                    for item in initial_records_of_authors
                ]
            )

        # Создаём таблицу books, если её нет
        cursor.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{BOOKS_TABLE_NAME}';"
        )
        exists_books = cursor.fetchone()
        if not exists_books:
            cursor.executescript(
                f"""
                CREATE TABLE `{BOOKS_TABLE_NAME}`(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT,
                    author_id INTEGER NOT NULL,
                    FOREIGN KEY(author_id) REFERENCES `{AUTHORS_TABLE_NAME}`(id) ON DELETE CASCADE
                );
                """
            )
            cursor.executemany(
                f"""
                INSERT INTO `{BOOKS_TABLE_NAME}`
                (title, author_id) VALUES (?, ?)
                """,
                [
                    (item['title'], item['author_id'])
                    for item in initial_records
                ]
            )
        conn.commit()

def _get_book_obj_from_row(row: tuple) -> Book:
    return Book(id=row[0], title=row[1], author_id=row[2])


def get_all_books() -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{BOOKS_TABLE_NAME}`')
        all_books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in all_books]


def add_book(book: Book) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{BOOKS_TABLE_NAME}` 
            (title, author_id) VALUES (?, ?)
            """,
            (book.title, book.author_id)
        )
        book.id = cursor.lastrowid
        return book


def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE id = ?
            """,
            (book_id,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def update_book_by_id(book: Book) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE {BOOKS_TABLE_NAME}
            SET title = ?, author_id = ?
            WHERE id = ?
            """,
            (book.title, book.author_id, book.id)
        )
        conn.commit()


def delete_book_by_id(book_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {BOOKS_TABLE_NAME}
            WHERE id = ?
            """,
            (book_id,)
        )
        conn.commit()


def get_book_by_title(book_title: str) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE title = ?
            """,
            (book_title,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)
