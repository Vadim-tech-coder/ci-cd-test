import sqlite3

if __name__ == "__main__":
    with sqlite3.connect("hw_3_database.db") as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*)  FROM `table_1`")

        count_for_table1 = cursor.fetchall()

        cursor.execute("SELECT COUNT(*)  FROM `table_2`")

        count_for_table2 = cursor.fetchall()

        cursor.execute("SELECT COUNT(*)  FROM `table_3`")

        count_for_table3 = cursor.fetchall()

        cursor.execute("SELECT DISTINCT COUNT(*)  FROM `table_1`")

        count_unique_for_table1 = cursor.fetchall()

        cursor.execute("""SELECT COUNT(*) FROM
        (SELECT * FROM table_1
        INTERSECT
        SELECT * FROM table_2)""")

        count_intersect_for_table1_and_table2 = cursor.fetchall()

        cursor.execute("""SELECT COUNT(*) FROM 
                        (SELECT id, value FROM table_1  t1
                        INTERSECT 
                        SELECT t2.id, t2.value FROM 
                        table_2 t2 join table_3 t3 on t2.id = t3.id)""")

        count_intersect_for_table1_and_table2_and_3 = cursor.fetchall()

        print("Количество записей \nв таблице 1: ", count_for_table1[0][0], '\n' +
              "в таблице 2: ", count_for_table2[0][0], '\n' +
              "в таблице 3: ", count_for_table3[0][0],
              '\nКоличество уникальных записей в таблице 1: ', count_unique_for_table1[0][0],
              '\nКоличество записей таблицы 1 встречающихся в таблице 2: ', count_intersect_for_table1_and_table2[0][0],
              '\nКоличество записей таблицы 1 встречающихся в таблице 2 и 3: ',count_intersect_for_table1_and_table2_and_3[0][0])
