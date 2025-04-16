import unittest
from module_03_ci_culture_beginning.homework.hw2.decrypt import decrypt


dict_of_parameters = {
'абра-кадабра.' : 'абра-кадабра',

'абраа..-кадабра' : 'абра-кадабра',

'абраа..-.кадабра' : 'абра-кадабра',

'абра--..кадабра' : 'абра-кадабра',

'абрау...-кадабра' : 'абра-кадабра',

'абра........' : '',

'абр......a.' : 'a',

'1..2.3' : '23',

'.' : '',

'1.......................' : ''
}

class TestDecrypt(unittest.TestCase):

    def test_decrypt(self):
        for key, value in dict_of_parameters.items():
            with self.subTest():
                result = decrypt(key)
                print(f"Сравниваем: {result} и {value}")
                self.assertEqual(result, value, f"Значение посчитанное функцией: {result} не равно"
                                                f" ожидаемому значению: {value}")