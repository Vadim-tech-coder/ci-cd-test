"""
Для каждого поля и валидатора в эндпоинте /registration напишите юнит-тест,
который проверит корректность работы валидатора. Таким образом, нужно проверить, что существуют наборы данных,
которые проходят валидацию, и такие, которые валидацию не проходят.
"""
import json
import unittest
from hw1_registration import app

class TestValidationOfRegistrationFields(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.base_url = '/registration'

    def test_correct_email(self):
        """
        Функция для првоерки успешной работы с корректным email
        """
        email = "vadimbaz25@gmail.com"
        phone = 1234567890
        request_body = {"email": email,
                        "name": "Вадим",
                        "phone": phone,
                        "address": "на деревню дедушке",
                        "index": 455045,
                        "comment": "Вход с двора"
                        }
        request_header = {"Content-type": "application/json"}

        response = self.app.post(self.base_url, headers=request_header, data=json.dumps(request_body))

        response_text = response.data.decode()
        resp_code = response.status_code
        expected_message = f"Successfully registered user {email} with phone +7{phone}"
        expected_resp_code = 200
        self.assertEqual(expected_message, response_text)
        self.assertEqual(resp_code, expected_resp_code)

    def test_wrong_email(self):
        """
        Функция для проверки НЕуспешной работы с email не по формату
        """
        email = "vadimbaz25gmail.com"
        phone = 1234567890
        request_body = {"email": email,
                        "name": "Вадим",
                        "phone": phone,
                        "address": "на деревню дедушке",
                        "index": 455045,
                        "comment": "Вход с двора"
                        }
        request_header = {"Content-type": "application/json"}

        response = self.app.post(self.base_url, headers=request_header, data=json.dumps(request_body))

        response_text = response.data.decode()
        resp_code = response.status_code
        expected_message = "Invalid input, {'email': ['Поле email не соответствует формату!']}"
        expected_resp_code = 400
        self.assertEqual(expected_message, response_text)
        self.assertEqual(resp_code, expected_resp_code)


    def test_empty_email(self):
        """
        Функция для проверки НЕуспешной работы с пустым email
        """

        email = ""
        phone = 1234567890
        request_body = {"email": email,
                        "name": "Вадим",
                        "phone": phone,
                        "address": "на деревню дедушке",
                        "index": 455045,
                        "comment": "Вход с двора"
                        }
        request_header = {"Content-type": "application/json"}

        response = self.app.post(self.base_url, headers=request_header, data=json.dumps(request_body))

        response_text = response.data.decode()
        resp_code = response.status_code
        expected_message = "Invalid input, {'email': ['Поле email обязательно для ввода!']}"
        expected_resp_code = 400
        self.assertEqual(expected_message, response_text)
        self.assertEqual(resp_code, expected_resp_code)


    def test_correct_phone(self):
        """
        Функция для проверки успешной работы с корректным номером телефона
        """
        email = "vadimbaz25@gmail.com"
        phone = 9998887766
        request_body = {"email": email,
                        "name": "Вадим",
                        "phone": phone,
                        "address": "на деревню дедушке",
                        "index": 455045,
                        "comment": "Вход с двора"
                        }
        request_header = {"Content-type": "application/json"}

        response = self.app.post(self.base_url, headers=request_header, data=json.dumps(request_body))

        response_text = response.data.decode()
        resp_code = response.status_code
        expected_message = f"Successfully registered user {email} with phone +7{phone}"
        expected_resp_code = 200
        self.assertEqual(expected_message, response_text)
        self.assertEqual(resp_code, expected_resp_code)


    def test_empty_phone(self):
        """
        Функция для проверки НЕуспешной работы с пустым номером телефона
        """
        email = "vadimbaz25@gmail.com"
        phone = 9998887766
        request_body = {"email": email,
                        "name": "Вадим",
                        "address": "на деревню дедушке",
                        "index": 455045,
                        "comment": "Вход с двора"
                        }
        request_header = {"Content-type": "application/json"}

        response = self.app.post(self.base_url, headers=request_header, data=json.dumps(request_body))

        response_text = response.data.decode()
        resp_code = response.status_code
        expected_message = "Invalid input, {'phone': ['This field is required.']}"
        expected_resp_code = 400
        self.assertEqual(expected_message, response_text)
        self.assertEqual(resp_code, expected_resp_code)


    def test_phone_len_less_10(self):
        """
        Функция для проверки НЕуспешной работы с номером телефона меньше 10 символов
        """
        email = "vadimbaz25@gmail.com"
        phone = 999888
        request_body = {"email": email,
                        "name": "Вадим",
                        "phone": phone,
                        "address": "на деревню дедушке",
                        "index": 455045,
                        "comment": "Вход с двора"
                        }
        request_header = {"Content-type": "application/json"}

        response = self.app.post(self.base_url, headers=request_header, data=json.dumps(request_body))

        response_text = response.data.decode()
        resp_code = response.status_code
        expected_message = "Invalid input, {'phone': ['Длина поля phone равна 6 не входит в диапазон валидатора функции от 10 до 10']}"
        expected_resp_code = 400
        self.assertEqual(expected_message, response_text)
        self.assertEqual(resp_code, expected_resp_code)


    def test_phone_len_more_10(self):
        """
        Функция для проверки НЕуспешной работы с номером телефона больше 10 символов
        """
        email = "vadimbaz25@gmail.com"
        phone = 999888776655
        request_body = {"email": email,
                        "name": "Вадим",
                        "phone": phone,
                        "address": "на деревню дедушке",
                        "index": 455045,
                        "comment": "Вход с двора"
                        }
        request_header = {"Content-type": "application/json"}

        response = self.app.post(self.base_url, headers=request_header, data=json.dumps(request_body))

        response_text = response.data.decode()
        resp_code = response.status_code
        expected_message = "Invalid input, {'phone': ['Длина поля phone равна 12 не входит в диапазон валидатора функции от 10 до 10']}"
        expected_resp_code = 400
        self.assertEqual(expected_message, response_text)
        self.assertEqual(resp_code, expected_resp_code)


    def test_empty_name(self):
        """
        Функция для проверки НЕуспешной работы с пустым полем name
        """
        email = "vadimbaz25@gmail.com"
        phone = 9998887766
        request_body = {"email": email,
                        "phone": phone,
                        "address": "на деревню дедушке",
                        "index": 455045,
                        "comment": "Вход с двора"
                        }
        request_header = {"Content-type": "application/json"}

        response = self.app.post(self.base_url, headers=request_header, data=json.dumps(request_body))

        response_text = response.data.decode()
        resp_code = response.status_code
        expected_message = "Invalid input, {'name': ['This field is required.']}"
        expected_resp_code = 400
        self.assertEqual(expected_message, response_text)
        self.assertEqual(resp_code, expected_resp_code)


    def test_name_less_3_symbols(self):
        """
        Функция для проверки НЕуспешной работы с полем name меньше 2-х символов
        """
        email = "vadimbaz25@gmail.com"
        phone = 9998887766
        name = "В"
        request_body = {"email": email,
                        "phone": phone,
                        "name": name,
                        "address": "на деревню дедушке",
                        "index": 455045,
                        "comment": "Вход с двора"
                        }
        request_header = {"Content-type": "application/json"}

        response = self.app.post(self.base_url, headers=request_header, data=json.dumps(request_body))

        response_text = response.data.decode()
        resp_code = response.status_code
        expected_message = "Invalid input, {'name': ['Длина поля не входит в диапазон валидатора класса от 2 до 50']}"
        expected_resp_code = 400
        self.assertEqual(expected_message, response_text)
        self.assertEqual(resp_code, expected_resp_code)

    def test_empty_address(self):
        """
        Функция для проверки НЕуспешной работы с пустым адресом
        """
        email = "vadimbaz25@gmail.com"
        phone = 9998887766
        request_body = {"email": email,
                        "name": "Вадим",
                        "phone": phone,
                        "index": 455045,
                        "comment": "Вход с двора"
                        }
        request_header = {"Content-type": "application/json"}

        response = self.app.post(self.base_url, headers=request_header, data=json.dumps(request_body))

        response_text = response.data.decode()
        resp_code = response.status_code
        expected_message = "Invalid input, {'address': ['This field is required.']}"
        expected_resp_code = 400
        self.assertEqual(expected_message, response_text)
        self.assertEqual(resp_code, expected_resp_code)

    def test_empty_index(self):
        """
        Функция для проверки НЕуспешной работы с пустым индексом
        """
        email = "vadimbaz25@gmail.com"
        phone = 9998887766
        request_body = {"email": email,
                        "name": "Вадим",
                        "phone": phone,
                        "address": "На деревню дедушке",
                        "comment": "Вход с двора"
                        }
        request_header = {"Content-type": "application/json"}

        response = self.app.post(self.base_url, headers=request_header, data=json.dumps(request_body))

        response_text = response.data.decode()
        resp_code = response.status_code
        expected_message = "Invalid input, {'index': ['This field is required.']}"
        expected_resp_code = 400
        self.assertEqual(expected_message, response_text)
        self.assertEqual(resp_code, expected_resp_code)


    def test_index_is_not_number(self):
        """
        Функция для проверки НЕуспешной работы с полем индекс в видео текста
        """
        email = "vadimbaz25@gmail.com"
        phone = 9998887766
        request_body = {"email": email,
                        "name": "Вадим",
                        "phone": phone,
                        "address": "На деревню дедушке",
                        "comment": "Вход с двора",
                        "index": "четыресто пятьдесят девять"
                        }
        request_header = {"Content-type": "application/json"}

        response = self.app.post(self.base_url, headers=request_header, data=json.dumps(request_body))

        response_text = response.data.decode()
        resp_code = response.status_code
        expected_message = "Invalid input, {'index': ['Not a valid integer value.']}"
        expected_resp_code = 400
        self.assertEqual(expected_message, response_text)
        self.assertEqual(resp_code, expected_resp_code)


    def test_empty_comment(self):
        """
        Функция для проверки успешной работы с пустым полем comment
        """
        email = "vadimbaz25@gmail.com"
        phone = 9998887766
        request_body = {"email": email,
                        "name": "Вадим",
                        "phone": phone,
                        "index": 455045,
                        "address": "На деревню дедушке"
                        }
        request_header = {"Content-type": "application/json"}

        response = self.app.post(self.base_url, headers=request_header, data=json.dumps(request_body))

        response_text = response.data.decode()
        resp_code = response.status_code
        expected_message = "Successfully registered user vadimbaz25@gmail.com with phone +79998887766"
        expected_resp_code = 200
        self.assertEqual(expected_message, response_text)
        self.assertEqual(resp_code, expected_resp_code)

    def test_comment_as_numbers(self):
        """
        Функция для проверки успешной работы с числом, переденным в поле comment
        """
        email = "vadimbaz25@gmail.com"
        phone = 9998887766
        request_body = {"email": email,
                        "name": "Вадим",
                        "phone": phone,
                        "index": 455045,
                        "address": "На деревню дедушке",
                        "comment": 123456789
                        }
        request_header = {"Content-type": "application/json"}

        response = self.app.post(self.base_url, headers=request_header, data=json.dumps(request_body))

        response_text = response.data.decode()
        resp_code = response.status_code
        expected_message = "Successfully registered user vadimbaz25@gmail.com with phone +79998887766"
        expected_resp_code = 200
        self.assertEqual(expected_message, response_text)
        self.assertEqual(resp_code, expected_resp_code)


if __name__ == '__main__':

    unittest.main()
