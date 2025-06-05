import sqlite3
from typing import Any, Optional, List

DATA: List[dict] = [
    {'id': 0, 'title': 'A Byte of Python', 'author': 'Swaroop C. H.', 'views': 1},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 'Herman Melville', 'views': 0},
    {'id': 3, 'title': 'War and Peace', 'author': 'Leo Tolstoy', 'views': 0},
]


class Book:

    def __init__(self, id: int, title: str, author: str, views: int) -> None:
        self.id: int = id
        self.title: str = title
        self.author: str = author
        self.views: int = views

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


def init_db(initial_records: List[dict]) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='table_books'; 
            """
        )
        exists: Optional[tuple[str,]] = cursor.fetchone()
        # now in `exist` we have tuple with table name if table really exists in DB
        if not exists:
            cursor.executescript(
                """
                CREATE TABLE `table_books` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT, 
                    author TEXT,
                    views INTEGER
                )
                """
            )
            cursor.executemany(
                """
                INSERT INTO `table_books`
                (title, author, views) VALUES (?, ?, ?)
                """,
                [
                    (item['title'], item['author'], item['views'])
                    for item in initial_records
                ]
            )


def get_all_books_for_author(author:str) -> List[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM 'table_books' WHERE author LIKE ?", (f'%{author}%', ))
        all_books = cursor.fetchall()
        return [Book(*row) for row in all_books]


def get_book_by_id(id: int) -> List[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM 'table_books' WHERE id = ?", (id,))
        book = cursor.fetchone()
        if book:
            current_view_count = cursor.execute("SELECT views FROM 'table_books' WHERE id = ?", (id,))
            increased_view_count = current_view_count.fetchone()[0] + 1
            cursor.execute("UPDATE table_books SET views = ? WHERE id = ?", (increased_view_count, id))
            conn.commit()
        return [Book(*book)] if book else []


def get_all_books() -> List[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * from `table_books`
            """
        )
        return [Book(*row) for row in cursor.fetchall()]


def add_new_book(title: str, author: str) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO table_books
        (title, author, views) VALUES (?, ?, ?)
        """, (title, author, 0, ))