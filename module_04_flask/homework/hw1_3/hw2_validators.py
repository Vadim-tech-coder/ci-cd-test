"""
Довольно неудобно использовать встроенный валидатор NumberRange для ограничения числа по его длине.
Создадим свой для поля phone. Создайте валидатор обоими способами.
Валидатор должен принимать на вход параметры min и max — минимальная и максимальная длина,
а также опциональный параметр message (см. рекомендации к предыдущему заданию).
"""
from typing import Optional

from flask_wtf import FlaskForm
from wtforms import Field
from wtforms.validators import ValidationError


def number_length(min: int, max: int, message: Optional[str] = None):

    def _number_length(form: FlaskForm, field: Field):
        if isinstance(field.data, int):
            data = str(field.data)
        else:
            data = field.data
        field_length = len(data)
        if field_length < min or field_length > max:
            raise ValidationError(f"Длина поля {field.name} равна {field_length} не входит в диапазон валидатора"
                                  f" функции от {min} до {max}")
    return _number_length


class NumberLength:

    def __init__(self, min: int, max: int, message: Optional[str] = None):
        self.min = min
        self.max = max
        if not message:
            message = f"Длина поля не входит в диапазон валидатора класса от {self.min} до {self.max}"
        self.message = message

    def __call__(self, form, field):
        if isinstance(field.data, int):
            data = str(field.data)
        else:
            data = field.data
        field_length = len(data)
        if field_length < self.min or field_length > self.max:
            raise ValidationError(self.message)