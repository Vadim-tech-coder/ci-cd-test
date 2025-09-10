"""
Реализуйте контекстный менеджер, который будет игнорировать переданные типы исключений, возникающие внутри блока with.
Если выкидывается неожидаемый тип исключения, то он прокидывается выше.
"""

from typing import Collection, Type, Literal
from types import TracebackType


class BlockErrors:
    def __init__(self, errors: Collection) -> None:
        self.errors_dict = errors

    def __enter__(self) -> None:
        ...

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> Literal[True] | None:
        if issubclass(exc_type, tuple(self.errors_dict)) or exc_type in self.errors_dict:
            return True

if __name__ == "__main__":
    err_types = {ZeroDivisionError, TypeError}
    with BlockErrors(err_types):
        a = 1 / 0
    print('Пример №1. Выполнено без ошибок')

    outer_err_types = {TypeError}
    with BlockErrors(outer_err_types):
        inner_err_types = {ZeroDivisionError}
        with BlockErrors(inner_err_types):
            a = 1 / '0'
        print('Пример №3. Внутренний блок: выполнено без ошибок')
    print('Пример №3. Внешний блок: выполнено без ошибок')

    err_types = {Exception}
    with BlockErrors(err_types):
        a = 1 / '0'
    print('Пример №4. Выполнено без ошибок')

    err_types = {ZeroDivisionError}
    with BlockErrors(err_types):
        a = 1 / '0'
    print('Пример №2. Выполнено без ошибок')


