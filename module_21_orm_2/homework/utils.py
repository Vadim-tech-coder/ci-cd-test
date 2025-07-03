

def str_to_bool(value):
    """
    Функция для преобразования строковых значений в булевое.
    """
    if isinstance(value, bool):
        return value
    if not isinstance(value, str):
        return False

    value = value.strip().lower()
    if value in ('true', '1', 'yes', 'y', 't'):
        return True
    elif value in ('false', '0', 'no', 'n', 'f'):
        return False
    else:
        raise ValueError(f"Cannot convert {value} to boolean")
