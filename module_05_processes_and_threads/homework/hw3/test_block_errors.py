import unittest
from block_errors import BlockErrors

class CustomTypeError(TypeError):
    pass

class TestBlockErrors(unittest.TestCase):

    def test_ignore_error(self):
        try:
            with BlockErrors({ZeroDivisionError}):
                a = 1 / 0
        except:
            self.fail("Ошибка деления на ноль проигнорирована")


    def test_error_raise(self):
        with self.assertRaises(ZeroDivisionError):
            with BlockErrors({TypeError}):
                a = 1 / 0

    def test_inner_exception(self):
        try:
            with BlockErrors({ZeroDivisionError}):
                with BlockErrors({TypeError}):
                    a = 1 / 0
        except:
            self.fail("Ошибка при проверке игнорирования ошибки из внутреннего блока.")

    def test_ignoring_children_exception(self):
        try:
            with BlockErrors({TypeError}):
                raise CustomTypeError
        except:
            self.fail("Ошибка при проверке дочернего исключения!")

if __name__ == '__main__':
    unittest.main()
