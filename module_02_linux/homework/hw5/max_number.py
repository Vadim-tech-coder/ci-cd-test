"""
Реализуйте endpoint, начинающийся с /max_number, в который можно передать список чисел, разделённых слешем /.
Endpoint должен вернуть текст «Максимальное переданное число {number}»,
где number — выделенное курсивом наибольшее из переданных чисел.

Примеры:

/max_number/10/2/9/1
Максимальное число: 10

/max_number/1/1/1/1/1/1/1/2
Максимальное число: 2

"""

from flask import Flask

app = Flask(__name__)


@app.route("/max_number/<path:numbers>")
def max_number(numbers):
    numbers_list = numbers.split('/')
    try:
        numbers_list_int = list(map(int, numbers_list))
        max_value = max(numbers_list_int)
        status_code = 200
        result = numbers.replace('/' + str(max_value), '<b>/' + str(max_value) + '</b>')
    except ValueError as err:
        result = "Передано не число, детали ошибки: " + str(err)
        status_code = 500
    return f"{result}", status_code


if __name__ == "__main__":
    app.run(debug=True)
