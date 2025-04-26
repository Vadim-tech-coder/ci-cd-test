"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""
import shlex
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
import subprocess
from shlex import quote

from wtforms.validators import InputRequired

app = Flask(__name__)


class CodeForm(FlaskForm):
    code = StringField(validators=[InputRequired()])
    timeout = IntegerField(validators=[InputRequired()])


def run_python_code_in_subproccess(code: str, timeout: int):
    command_line = f"python -c {quote(code)}"
    command_line_as_list = shlex.split(command_line)
    try:
        result = subprocess.run(command_line_as_list, capture_output=True, text=True, timeout=timeout)
        if result.returncode == 0:
            return f"Process was finished with code: {result.returncode}, Process result: {result.stdout}", 200
        else:
            return f"Error: Retuncode is {result.returncode}; stdERR: {result.stderr}", 400
    except subprocess.TimeoutExpired as err_timedout:
        return f"Timeout: {err_timedout}", 400
    except Exception as error_details:
        return f"Process failed, error: {error_details}", 400


@app.route('/run_code', methods=['POST'])
def run_code():
    form = CodeForm()
    if not form.validate_on_submit():
        return "Invalid input data", 400

    return run_python_code_in_subproccess(code = form.code.data, timeout = form.timeout.data)


if __name__ == '__main__':
    app.config['WTF_CSRF_ENABLED'] = False
    app.run(debug=True)
