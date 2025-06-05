from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired
from typing import List

from models import init_db, get_all_books, DATA, add_new_book, get_all_books_for_author

app: Flask = Flask(__name__)

class AddBookForm(FlaskForm):
    title = StringField(validators=[InputRequired("Поле Title обязательно для ввода!")])
    author = StringField(validators=[InputRequired("Поле Author обязательно для ввода!")])



def _get_html_table_for_books(books: List[dict]) -> str:
    table = """
<table>
    <thead>
    <tr>
        <th>ID</td>
        <th>Title</td>
        <th>Author</td>
    </tr>
    </thead>
    <tbody>
        {books_rows}
    </tbody>
</table>
"""
    rows: str = ''
    for book in books:
        rows += '<tr><td>{id}</tb><td>{title}</tb><td>{author}</tb></tr>'.format(
            id=book['id'], title=book['title'], author=book['author'],
        )
    return table.format(books_rows=rows)


@app.route('/books')
def all_books() -> str:
    return render_template(
        'index.html',
        books=get_all_books(),
    )


@app.route('/search/<author>')
def search_all_books_for_author(author: str) -> str:
    return render_template(
        'index.html',
        books=get_all_books_for_author(author),
    )



@app.route('/books/form', methods = ['post', 'get'])
def get_books_form() -> str:
    form = AddBookForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            author = form.author.data
            add_new_book(title, author)
        return redirect('/books')
    else:
        return render_template('add_book.html', form = form)


if __name__ == '__main__':
    init_db(DATA)
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
