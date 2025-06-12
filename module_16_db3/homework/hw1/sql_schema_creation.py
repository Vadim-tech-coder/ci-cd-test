import sqlite3

ENABLE_FOREIGN_KEY = "PRAGMA foreign_keys = ON;"

CREATE_ACTORS_TABLE = """
DROP TABLE IF EXISTS 'actors';
CREATE TABLE 'actors' (
    act_id INTEGER PRIMARY KEY AUTOINCREMENT,
    act_first_name VARCHAR(50) NOT NULL,
    act_last_name TEXT VARCHAR(50) NOT NULL,
    act_gender VARCHAR(1) NOT NULL
) 
"""

CREATE_MOVIE_TABLE = """
DROP TABLE IF EXISTS 'movie';
CREATE TABLE 'movie' (
    mov_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mov_title VARCHAR(50) NOT NULL
);
"""

CREATE_TABLE_DIRECTOR = """
DROP TABLE IF EXISTS 'director';
CREATE TABLE 'director' (
    dir_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dir_first_name VARCHAR(50) NOT NULL, 
    dir_last_name VARCHAR(50) NOT NULL 
)
"""


CREATE_TABLE_MOVIE_CAST = """
DROP TABLE IF EXISTS 'movie_cast';
CREATE TABLE 'movie_cast' (
    act_id INTEGER NOT NULL REFERENCES actors(act_id) ON DELETE CASCADE,
    mov_id INTEGER NOT NULL REFERENCES movie(mov_id) ON DELETE CASCADE, 
    role VARCHAR(50) NOT NULL,
    PRIMARY KEY(act_id, mov_id)
)
"""


CREATE_TABLE_OSCAR_AWARDED = """
DROP TABLE IF EXISTS 'oscar_awarded';
CREATE TABLE 'oscar_awarded' (
    award_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mov_id INTEGER NOT NULL,
    FOREIGN KEY(mov_id) REFERENCES movie(mov_id) ON DELETE CASCADE
);
"""


CREATE_TABLE_MOVIE_DIRECTION = """
DROP TABLE IF EXISTS 'movie_direction';
CREATE TABLE 'movie_direction' (
    dir_id INTEGER NOT NULL, 
    mov_id INTEGER NOT NULL,
    FOREIGN KEY(dir_id) REFERENCES director(dir_id),
    FOREIGN KEY(mov_id) REFERENCES movie(mov_id) 
    )
"""

def create_tables() -> None:
    with sqlite3.connect("surrogate_extra_link.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.executescript(ENABLE_FOREIGN_KEY)
        cursor.executescript(CREATE_ACTORS_TABLE)
        cursor.executescript(CREATE_MOVIE_TABLE)
        cursor.executescript(CREATE_TABLE_DIRECTOR)
        cursor.executescript(CREATE_TABLE_MOVIE_CAST)
        cursor.executescript(CREATE_TABLE_OSCAR_AWARDED)
        cursor.executescript(CREATE_TABLE_MOVIE_DIRECTION)


if __name__ == '__main__':
    create_tables()