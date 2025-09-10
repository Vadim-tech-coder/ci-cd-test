"""
Заменим сообщение "The requested URL was not found on the server" на что-то более информативное.
Например, выведем список всех доступных страниц с возможностью перехода по ним.

Создайте Flask Error Handler, который при отсутствии запрашиваемой страницы будет выводить
список всех доступных страниц на сайте с возможностью перехода на них.
"""
from werkzeug.exceptions import NotFound
from flask import Flask, url_for

app = Flask(__name__)


@app.route('/dogs')
def dogs():
    return 'Страница с пёсиками'


@app.route('/cats')
def cats():
    return 'Страница с котиками'


@app.route('/cats/<int:cat_id>')
def cat_page(cat_id: int):
    return f'Страница с котиком {cat_id}'


@app.route('/index')
def index():
    return 'Главная страница'


@app.errorhandler(NotFound)
def handle_exception(e: NotFound):
    site_links = []
    for rule in app.url_map.iter_rules():
        # Пропускаем правила без endpoint или с аргументами без значений по умолчанию
        if not rule.endpoint or rule.arguments:
            continue
        url = url_for(rule.endpoint, **(rule.defaults or {}))
        site_links.append(f'<li><a href="{url}">{rule.endpoint}</a></li>')

    links_html = "<ul>" + "".join(site_links) + "</ul>"
    return f"Такой страницы нет!<br>Список доступных страниц:<br>{links_html}", 404

if __name__ == '__main__':
    app.run(debug=True)
