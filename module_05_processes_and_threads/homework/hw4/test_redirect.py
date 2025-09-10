import unittest
from redirect import Redirect


class TestRedirect(unittest.TestCase):

    @classmethod
    def setUpClass(cls)->None:
        cls.stdout_text = 'stdout text'
        cls.stderr_text = 'stderr text'

    def test_stdout_stderr(self):

        """Функция для проверки успешной работы при задании обоих файлов stdout, stderr"""

        with open('test_stdout.txt', 'w') as stdout_file, open('test_stderr.txt', 'w') as stderr_file:
            with Redirect(stdout=stdout_file, stderr=stderr_file):
                print(self.stdout_text)
                raise Exception(self.stderr_text)

        with open('test_stdout.txt', "r") as stdout_file, open('test_stderr.txt', 'r') as stderr_file:
            stdout = stdout_file.read()
            stderr = stderr_file.read()
        self.assertIn(self.stdout_text, stdout)
        self.assertIn(self.stderr_text, stderr)


    def test_not_set_stdout_and_stderr(self):

        """Функция для проверки успешной работы, если не перехватывать потоки stdout, stderr"""

        with self.assertRaises(Exception):
            with open('test_stdout.txt', 'w') as stdout_file, open('test_stderr.txt', 'w') as stderr_file:
                with Redirect():
                    print(self.stdout_text)
                    raise Exception(self.stderr_text)

        with open('test_stdout.txt', "r") as stdout_file, open('test_stderr.txt', 'r') as stderr_file:
            stdout = stdout_file.read()
            stderr = stderr_file.read()
        self.assertIn("", stdout) #Проверяем, что в файлы ничего не записалось, пустая строка.
        self.assertIn("", stderr)


    def test_stderr_only(self):

        """Функция для проверки успешной работы при задании только файла stderr"""

        with open('test_stderr_only.txt', 'w') as stderr_file:
            with Redirect(stderr=stderr_file):
                print(self.stdout_text)
                raise Exception(self.stderr_text)

        with open('test_stderr_only.txt', 'r') as stderr_file:
            stderr = stderr_file.read()
        self.assertIn(self.stderr_text, stderr)

    def test_stdout_only(self):

        """Функция для проверки успешной работы при задании только файла stdout"""

        with open('test_stdout_only.txt', 'w') as stdout_file:
            with Redirect(stdout=stdout_file):
                print(self.stdout_text)

        with open('test_stdout_only.txt', 'r') as stdout_file:
            stdout = stdout_file.read()
        self.assertIn(self.stdout_text, stdout)

if __name__ == '__main__':
    unittest.main()
    # with open('test_results.txt', 'a') as test_file_stream:
    #     runner = unittest.TextTestRunner(stream=test_file_stream)
    #     unittest.main(testRunner=runner)
