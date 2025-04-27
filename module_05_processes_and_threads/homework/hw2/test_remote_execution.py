
import unittest
from remote_execution import app


class TestRemoteExcutionOfPythonCode(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.base_url = '/run_code'

    def test_success_command(self):
        """
        Функция для проверки успешной работы с корректной командой
        """
        code = "print('Hello, World!')"
        timeout = 5

        request_header = {"Content-type": "application/x-www-form-urlencoded"}
        request_body = {
            "code": code,
            "timeout": timeout
        }
        response = self.app.post(self.base_url, headers=request_header, data=request_body)

        response_text = response.data.decode()
        resp_code = response.status_code
        expected_message = f"Process was finished with code: 0, Process result: Hello, World!\n"
        expected_resp_code = 200
        self.assertEqual(expected_message, response_text)
        self.assertEqual(resp_code, expected_resp_code)


    def test_wrong_command(self):
        """
        Функция для проверки неуспешной работы с неподдерживаемой командой
        """
        code = "somecommand"
        timeout = 5

        request_header = {"Content-type": "application/x-www-form-urlencoded"}
        request_body = {
            "code": code,
            "timeout": timeout
        }
        response = self.app.post(self.base_url, headers=request_header, data=request_body)

        response_text = response.data.decode()
        resp_code = response.status_code
        expected_message = "NameError: name \'somecommand\' is not defined\n"
        expected_resp_code = 400
        self.assertIn(expected_message, response_text)
        self.assertEqual(resp_code, expected_resp_code)


    def test_exceed_timeout(self):
        """
        Функция для проверки неуспешной работы при превышении таймаута
        """
        code = """from time import sleep\nsleep(6)"""
        timeout = 5

        request_header = {"Content-type": "application/x-www-form-urlencoded"}
        request_body = {
            "code": code,
            "timeout": timeout
        }
        response = self.app.post(self.base_url, headers=request_header, data=request_body)

        response_text = response.data.decode()
        resp_code = response.status_code
        expected_message = "Timeout: Command '['python', '-c', 'from time import sleep\\nsleep(6)']' timed out after 5 seconds"
        expected_resp_code = 400
        self.assertIn(expected_message, response_text)
        self.assertEqual(resp_code, expected_resp_code)


if __name__ == '__main__':
    unittest.main()
