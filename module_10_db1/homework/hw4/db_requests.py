import  sqlite3
import statistics

if __name__ == '__main__':

    with sqlite3.connect('hw_4_database.db') as conn:

        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM salaries s WHERE salary < 5000 ")

        count_of_people_with_salary_less_5000 = cursor.fetchall()

        cursor.execute("""select ROUND(
                                (SELECT SUM(salary) 
                                FROM salaries s)/
                                (SELECT COUNT(*) 
                                FROM salaries s), 2)""")

        average_salary = cursor.fetchall()

        cursor.execute("SELECT salary FROM salaries s")

        all_salaries = [row[0] for row in cursor.fetchall()]
        median_salary = statistics.median(all_salaries)


        cursor.execute("""WITH RankedResidents AS (
        SELECT 
            s.salary, 
            NTILE(10) OVER (ORDER BY s.salary DESC) AS decile
        FROM salaries s
    ),
    AggregatedIncome AS (
        SELECT 
            SUM(CASE WHEN decile = 1 THEN salary ELSE 0 END) AS TOP_10_PERCENT_SALARY,
            SUM(CASE WHEN decile > 1 THEN salary ELSE 0 END) AS OTHER_90_PERCENT_SALARY
        FROM RankedResidents
    )
    SELECT 
        CASE 
            WHEN OTHER_90_PERCENT_SALARY = 0 THEN NULL
            ELSE ROUND((TOP_10_PERCENT_SALARY * 1.0 / OTHER_90_PERCENT_SALARY) * 100, 2)
        END AS social_coefficient
    FROM AggregatedIncome;
        """)

        social_coef = cursor.fetchall()

        print("Количество человек с зарплатой ниже 5000: ", count_of_people_with_salary_less_5000[0][0],
              "\nСредняя зарплата: ", average_salary[0][0],
              "\nМедианная зарплата: ", median_salary,
              "\nКоэффициент социального неравенства: ", social_coef[0][0])