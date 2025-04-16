import unittest
from module_03_ci_culture_beginning.homework.hw4.person import Person
from datetime import datetime


class TestPerson(unittest.TestCase):
    def setUp(self):
        """Инициализируем обьект класса для каждого теста."""
        self.person = Person('Вадим', 1990, "Россия, Чел. обл., г. Магнитогорск, пр. К. Маркса")

    def test_set_name(self):
        """
        Функция для проверки установки нового имени.
        """
        self.person.set_name("Иван")
        self.assertEqual(self.person.get_name(), 'Иван')

    def test_get_name(self):
        """
        Функция для проверки получения имени.
        """
        new_name = self.person.get_name()
        expected_name = 'Вадим'
        self.assertEqual(new_name, expected_name, f"Новое имя: {new_name} не равно "
                                                  f"ожидаемому: {expected_name}")

    def test_get_age(self):
        """
        Функция для проверки получения возраста.
        """
        age = self.person.get_age()
        current_year = datetime.now().year
        expected_age = current_year - self.person.yob
        self.assertEqual(age, expected_age, f"Полученный возраст: {age} не равен "
                                                  f"ожидаемому: {expected_age}")

    def test_set_address(self):
        """
        Функция для проверки установки адреса.
        """
        new_address = "г. Москва, пр. Мира, д. 55"
        self.person.set_address(new_address)
        self.assertEqual(self.person.get_address(), new_address, f"Новый адрес человека: {self.person.get_address()} не равен "
                                                  f"ожидаемому: {new_address}")

    def test_get_address(self):
        """
        Функция для проверки получения адреса.
        """
        client_address = self.person.get_address()
        expected_address = "Россия, Чел. обл., г. Магнитогорск, пр. К. Маркса"
        self.assertEqual(client_address, expected_address, f"Адрес человека: {client_address} не равен "
                                                  f"ожидаемому: {expected_address}")

    def test_is_homeless_true(self):
        """
        Функция возращает True при отсутствии атрибута адрес.
        """
        self.person.set_address(None)
        self.assertTrue(self.person.is_homeless())

    def test_is_homeless_false(self):
        """
        Функция возращает False при наличии атрибута адрес.
        """
        self.assertFalse(self.person.is_homeless())