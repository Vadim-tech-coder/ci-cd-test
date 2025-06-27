import datetime
from flask import Flask, request, jsonify
from module_20_orm_1.homework.library_models import Base, session, Book, engine, ReceivedBooks, Student


app = Flask(__name__)


@app.before_request
def before_request_function():
    Base.metadata.create_all(engine)


@app.route('/')
def library_main():
    return 'Main page of Library!'


@app.route('/books', methods = ['GET'])
def get_all_books():

    'Получаем список всех книг в БД.'

    books = session.query(Book).all()
    books_list = []
    for book in books:
        books_list.append(book.to_json())
    return jsonify(books_list=books_list), 200

@app.route('/books', methods = ['POST'])
def give_book_to_student():

    'Выдаем книгу студенту.'

    book_id = request.form.get('book_id', type = int)
    student_id = request.form.get('student_id', type = int)
    issued_book = ReceivedBooks(book_id = book_id, student_id = student_id)
    session.add(issued_book)
    session.commit()

    return "Книга успешно выдана", 201

@app.route('/books', methods = ['PATCH'])
def return_book():

    'Возвращаем книгув библиотеку.'

    book_id = request.form.get('book_id', type=int)
    student_id = request.form.get('student_id', type=int)
    date_of_return = datetime.datetime.now()
    returned_book = session.query(ReceivedBooks).filter(ReceivedBooks.book_id == book_id,
                                                        ReceivedBooks.student_id == student_id).one_or_none()
    if returned_book:
        session.query(ReceivedBooks).filter(ReceivedBooks.book_id == book_id,
                    ReceivedBooks.student_id == student_id).update({ReceivedBooks.date_of_return: date_of_return})
        session.commit()
        return 'Книга успешно возвращена!', 200
    else:
        return 'Связка книги и студента не найдена!', 404


@app.route('/debitors', methods = ['GET'])
def get_debitors():

    'Получаем список должников, которые не сдали книгу в течении 14 дней.'

    list_of_debitors = []
    debitors = session.query(ReceivedBooks).all()
    for debitor in debitors:
        if debitor.count_date_with_book > 14:
            student = session.query(Student).filter(Student.id == debitor.student_id).one_or_none()
            list_of_debitors.append(student.to_json())
    return jsonify(list_of_debitors = list_of_debitors), 200


@app.route('/find', methods=['POST'])
def search_book():

    'Поиск книги по названию.'

    search_request = request.form.get('search_request', type = str).capitalize()
    search_request_as_sql = '%{}%'.format(search_request)
    found_books = session.query(Book).filter(Book.name.like(search_request_as_sql)).all()
    books_list = []
    for book in found_books:
        books_list.append(book.to_json())
    return jsonify(books_list=books_list), 200


if __name__ == '__main__':
    app.run()
