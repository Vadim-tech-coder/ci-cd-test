import unittest
from module_03_ci_culture_beginning.homework.hw3.accounting import app, add, calculate_month,calculate_year, storage

class TestAccounting(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        cls.app = app.test_client()
        storage.update({'2025':{'01':1300, '02': 1100, '03':1100, 'total':3500},
                       '2024':{'05':1300, '06': 1100, '07':1100, 'total':3500},
                       '2023':{'08':1300, '09': 1100, '10':1100, 'total':3500}})


    def test_add_new_year_record(self):

        """Функция проверяет добавление записи."""

        test_date = '20220101'
        expense = 1500
        self.app.get(f'/add/{test_date}/{expense}')
        self.assertEqual(storage[test_date[0:4]][test_date[4:6]], expense, f"Значение записанное в словарь"
                                                                    f" {storage[test_date[0:4]][test_date[4:6]]}"
                                                                    f"не равно переданному в тесте: {expense}")

    def test_add_wrong_year_record(self):
        """
        Функция для проверки неверно введенного года(год не состоит из 4-х символов).
        """
        test_date = '25'
        expense = 1500
        with self.assertRaises(ValueError):
            self.app.get(f'/add/{test_date}/{expense}')

    def test_calculate_exist_year(self):

        """Функция для проверки возвращаемого значения по существующему году. """

        test_year = '2022'
        expense = 1500
        self.app.get(f'/calculate/{test_year}')
        self.assertEqual(storage[test_year]['total'], expense, f"Траты за {test_year} в словаре: "
                                                                    f" {storage[test_year]['total']} "
                                                                    f"не равны переданному в тесте: {expense}")

    def test_calculate_not_exist_year(self):

        """Функция для проверки получения значения по несуществующему году в словаре."""

        test_year = '2001'
        self.app.get(f'/calculate/{test_year}')
        with self.assertRaises(KeyError):
            result_for_year = storage[test_year]['total']


    def test_calculate_exist_year_and_month(self):

        """Функция для проверки получения записи по существующему году и месяцу."""

        test_year = '2022'
        test_month = '01'
        expected_expenses = 1500
        self.app.get(f'/calculate/{test_year}/{test_month}')
        self.assertEqual(storage[test_year][test_month], expected_expenses, f"Значение записанное в словарь"
                                                                           f" {storage[test_year][test_month]}"
                                                                           f"не равно переданному в тесте: "
                                                                           f"{expected_expenses}")

    def test_calculate_exist_year_and_non_exist_month(self):

        """Функция для проверки получения записи по существующему году и несуществующему месяцу."""

        test_year = '2025'
        test_month = '12'
        self.app.get(f'/calculate/{test_year}/{test_month}')
        with self.assertRaises(KeyError):
            result_for_year = storage[test_year][test_month]