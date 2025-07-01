import calendar
from datetime import datetime, date
from flask import Flask, request, jsonify
from sqlalchemy import func

from module_21_orm_2.homework.library_models import Base, engine, session, Book, ReceivedBooks, Student

app = Flask(__name__)

@app.before_request
def before_request_function():
    Base.metadata.create_all(engine)


@app.route('/')
def library_main():
    return 'Main page of Library!'


@app.route('/books/', methods = ['GET'])
def get_all_books():

    'Получаем список всех книг в БД.'

    books = session.query(Book).all()
    books_list = []
    for book in books:
        books_list.append(book.to_json())
    return jsonify(books_list=books_list), 200

@app.route('/count_by_author_id/<int:author_id>', methods = ['GET'])
def get_all_books_by_author(author_id):

    'Получаем количество всех книг автора в БД.'

    books_count = session.query(func.sum(Book.count)).filter(Book.author_id == author_id).scalar()
    if books_count:
        return f"Осталось {books_count} книг автора с ид. {author_id}", 200
    else:
        return f"Для автора с ид. {author_id} не найдено книг", 404


@app.route('/book_recommendation/<int:student_id>', methods = ['GET'])
def get_book_recommendation(student_id):
    """
    Получиаем список книг, которые студент не читал, при этом другие книги этого
    автора студент уже брал (GET — входной параметр — ID студента).
    """
    books = session.query(ReceivedBooks.book_id).filter(ReceivedBooks.student_id == student_id)
    authors = session.query(Book.author_id).where(Book.id.in_(books))
    recommend_books = session.query(Book).where(Book.id.not_in(books)).where(Book.author_id.in_(authors)).all()
    book_list = []
    for book in recommend_books:
        book_list.append(book.to_json())

    if len(book_list) > 0:
        return jsonify(book_list=book_list), 200
    else:
        return f"Рекомендаций не найдено, читайте больше!", 404

@app.route('/average_by_month/<int:month>', methods = ['GET'])
def get_average_number_of_books_by_month(month):
    """
    Получить среднее количество книг, которые студенты брали в этом месяце (GET);
    """
    days = calendar.monthrange(datetime.now().year, month)[1]
    books_count_by_month = session.query(ReceivedBooks.id).filter(ReceivedBooks.date_of_issue.between(
        date(2025, month, 1), date(2025, month, days))).all()
    students_count = session.query(ReceivedBooks.student_id).filter(ReceivedBooks.date_of_issue.between(
        date(2025, month, 1), date(2025, month, days))).distinct().all()
    if books_count_by_month and students_count:
        average_by_month = round(len(books_count_by_month)/len(students_count), 2)
        return (f"Было взято книг {len(books_count_by_month)} в месяце #{month}, количество студентов = {len(students_count)}, "
                f"среднее арифметическое = {average_by_month}"), 200
    else:
        return f"В месяце #{month} не было выдано книг!", 404


@app.route('/top10_readers', methods = ['GET'])
def get_10_most_reading_students():
    """
    Получить ТОП-10 самых читающих студентов в этом году (GET).
    """
    count_by_students =  session.query(Student).where(Student.id.in_(
        session.query(func.count(ReceivedBooks.id)).filter(ReceivedBooks.date_of_issue.between(
        date(2025, 1, 1), date(2025, 12, 31))).group_by(ReceivedBooks.student_id).order_by(
        func.count(ReceivedBooks.id).desc()).limit(10))
    ).all()

    student_list = []
    # print(count_by_students)
    for student in count_by_students:
        student_list.append(student.to_json())
    return jsonify(student_list=student_list), 200


@app.route('/popular_book', methods = ['GET'])
def get_the_most_popular_book():
    """
    Получить самую популярную книгу среди студентов, у которых средний балл больше 4.0 (GET);
    """
    books = session.query(ReceivedBooks.book_id, func.count(ReceivedBooks.book_id)
                          ).where(ReceivedBooks.student_id.in_(
        session.query(Student.id).where(Student.average_score > 4)
    )).group_by(ReceivedBooks.id).all()
    popular_book_id = max(books, key = lambda book:book[1])[0]
    popular_book_title = session.query(Book.name).where(Book.id == popular_book_id).one_or_none()
    if popular_book_id:
        return f"Самая популярная книга с ид. {popular_book_id} называется '{popular_book_title[0]}'", 200
    else:
        return f"Не удалось найти самую популярную книгу!", 500



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



