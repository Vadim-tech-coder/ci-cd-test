"""
Напишите GET-эндпоинт /ps, который принимает на вход аргументы командной строки,
а возвращает результат работы команды ps с этими аргументами.
Входные значения эндпоинт должен принимать в виде списка через аргумент arg.

Например, для исполнения команды ps aux запрос будет следующим:

/ps?arg=a&arg=u&arg=x
"""
import shlex
import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def ps() -> str:
    get_args: list[str] = request.args.getlist('arg')
    if get_args:
        args = shlex.quote(''.join(elem for elem in get_args))
        result = subprocess.check_output(f"ps {args}", shell=True).decode()
    else:
        result = subprocess.check_output(f"ps", shell=True).decode()

    return f"<pre>{result}</pre>"



if __name__ == "__main__":
    app.run(debug=True)
