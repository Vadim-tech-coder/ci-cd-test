"""
Реализуйте приложение для учёта финансов, умеющее запоминать, сколько денег было потрачено за день,
а также показывать затраты за отдельный месяц и за целый год.

В программе должно быть три endpoints:

/add/<date>/<int:number> — сохранение информации о совершённой в рублях трате за какой-то день;
/calculate/<int:year> — получение суммарных трат за указанный год;
/calculate/<int:year>/<int:month> — получение суммарных трат за указанные год и месяц.

Дата для /add/ передаётся в формате YYYYMMDD, где YYYY — год, MM — месяц (от 1 до 12), DD — число (от 01 до 31).
Гарантируется, что переданная дата имеет такой формат и она корректна (никаких 31 февраля).
"""

from flask import Flask

app = Flask(__name__)

storage = {}


@app.route("/add/<date>/<int:number>")
def add(date: str, number: int):
    year = date[0:4]
    month = date[4:6]
    storage.setdefault(year, {}).setdefault(month, 0)
    storage.setdefault(year, {}).setdefault('total', 0)
    storage[year][month] += number
    storage[year]['total'] += number
    return "Траты в сумме: {} записаны в год {} месяц {} {}".format(number,
                                                                       year,
                                                                       month,
                                                                 storage)


@app.route("/calculate/<int:year>")
def calculate_year(year: int):
    print(storage)
    year_data = storage.get(str(year))
    if year_data is None:
        return "Данные за {} год отсутствуют!".format(year)
    return "Траты за {} год: {} рублей.".format(year, year_data.get('total', 0))


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    year_data = storage.get(str(year))
    if month < 10:
        month = "0" + str(month)
    if year_data is None:
        return "Данные за {} год отсутствуют!".format(year)
    month_data = year_data.get(str(month))
    if month_data is None:
        return "Данные за {} месяц отсутствуют!".format(month)
    return "Траты за год {} месяц {}: {}".format(year, month, month_data)


if __name__ == "__main__":
    app.run(debug=True)
