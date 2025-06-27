import datetime

from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Boolean, DateTime, case, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///library.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Book(Base):

    __tablename__ = 'books'

    id = Column(Integer, primary_key = True)
    name = Column(String(200), nullable = False)
    count = Column(Integer, default = 1)
    release_date = Column(Date, nullable = False)
    author_id = Column(Integer, nullable = False)


    def __repr__(self):
        return f"Книга: {self.name}, Количество: {self.count}, Дата выпуска: {self.release_date}"


    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Author(Base):

    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    surname = Column(String(200), nullable=False)

    def __repr__(self):
        return f"Автор имя: {self.name}, Автор фамилия: {self.surname}"

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Student(Base):

    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    surname = Column(String(200), nullable=False)
    phone = Column(String(15), nullable = False)
    email = Column(String(100), nullable=False)
    average_score = Column(Float, nullable = False)
    scholarship = Column(Boolean, nullable = False)


    def __repr__(self):
        return (f"Студент имя: {self.name}, Студент фамилия: {self.surname}, Телефон: {self.phone}, Email: {self.email}"
                f"Средний балл: {self.average_score}, Стипендия: {self.scholarship}")

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def get_students_with_scholarship(cls):
        students =  session.query(Student).filter(Student.scholarship == True).all()
        students_list = []
        for student in students:
            students_list.append(student.to_json())
        return students_list


    @classmethod
    def get_students_by_average_score(cls, score: int):
        students = session.query(Student).filter(Student.average_score > score).all()
        students_list = []
        for student in students:
            students_list.append(student.to_json())
        return students_list


class ReceivedBooks(Base):

    __tablename__ = 'receiving_books'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable = False)
    student_id = Column(Integer, nullable = False)
    date_of_issue = Column(DateTime, nullable = False, default = datetime.datetime.now())
    date_of_return = Column(DateTime, nullable = True)


    @hybrid_property
    def count_date_with_book(self):
        end_date = self.date_of_return or datetime.datetime.now()
        return (end_date - self.date_of_issue).days

    @count_date_with_book.expression
    def count_date_with_book(cls):
        end_date = case(
            (cls.date_of_return != None, cls.date_of_return),
            else_ = func.now()
        )
        return func.julianday(end_date) - func.julianday(cls.date_of_issue)

    def __repr__(self):
        return (f"ID книги: {self.book_id}, ID студента: {self.student_id}, Дата выдачи: {self.date_of_issue}, "
                f"Дата возврата: {self.date_of_return}")

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}





