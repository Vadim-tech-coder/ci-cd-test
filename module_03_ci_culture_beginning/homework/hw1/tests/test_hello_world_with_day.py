import unittest
from freezegun import freeze_time
from module_03_ci_culture_beginning.homework.hw1.hello_word_with_day import hello_world

class TestHelloWorldWithDay(unittest.TestCase):

    @freeze_time("2025-04-14")
    def test_monday_is_correct(self):
        name = 'Вадим'
        result_string = hello_world(name)
        expected_value = 'понедельник'
        self.assertIn(expected_value, result_string[12:], f"Ошибка: последние 12 символов строки - {result_string}"
                                                          f" не содержат подстроку: {expected_value}")

    @freeze_time("2025-04-15")
    def test_monday_in_name(self):
        """
        Функция проверяет, что даже если в имени пользователя есть день недели(понедельник),
        то часть строки с привествием пользователя не входит в проверку на текущий день недели.
        """
        name = 'понедельник'
        result_string = hello_world(name)
        expected_value = 'понедельник'
        self.assertNotIn(expected_value, result_string[12:], f"Ошибка: последние 12 символов строки - {result_string}"
                                                          f" не содержат подстроку: {expected_value}")

    @freeze_time("2025-04-15")
    def test_tuesday_is_correct(self):
        name = 'Вадим'
        result_string = hello_world(name)
        expected_value = 'вторник'
        self.assertIn(expected_value, result_string[12:], f"Ошибка: последние 12 символов строки - {result_string}"
                                                          f" не содержат подстроку: {expected_value}")

    @freeze_time("2025-04-16")
    def test_wednesday_is_correct(self):
        name = 'Вадим'
        result_string = hello_world(name)
        expected_value = 'среды'
        self.assertIn(expected_value, result_string[12:], f"Ошибка: последние 12 символов строки - {result_string}"
                                                          f" не содержат подстроку: {expected_value}")

    @freeze_time("2025-04-17")
    def test_thursday_is_correct(self):
        name = 'Вадим'
        result_string = hello_world(name)
        expected_value = 'четверга'
        self.assertIn(expected_value, result_string[12:], f"Ошибка: последние 12 символов строки - {result_string}"
                                                          f" не содержат подстроку: {expected_value}")

    @freeze_time("2025-04-18")
    def test_friday_is_correct(self):
        name = 'Вадим'
        result_string = hello_world(name)
        expected_value = 'пятницы'
        self.assertIn(expected_value, result_string[12:], f"Ошибка: последние 12 символов строки - {result_string}"
                                                          f" не содержат подстроку: {expected_value}")

    @freeze_time("2025-04-19")
    def test_saturday_is_correct(self):
        name = 'Вадим'
        result_string = hello_world(name)
        expected_value = 'субботы'
        self.assertIn(expected_value, result_string[12:], f"Ошибка: последние 12 символов строки - {result_string}"
                                                          f" не содержат подстроку: {expected_value}")

    @freeze_time("2025-04-20")
    def test_sunday_is_correct(self):
        name = 'Вадим'
        result_string = hello_world(name)
        expected_value = 'воскресенья'
        self.assertIn(expected_value, result_string[12:], f"Ошибка: последние 12 символов строки - {result_string}"
                                                          f" не содержат подстроку: {expected_value}")