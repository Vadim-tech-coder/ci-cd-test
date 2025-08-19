from flask import Flask
from models import Base, User
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select


app = Flask (__name__)

engine = create_engine(
    "postgresql+psycopg2://skillbox:skillbox@localhost:5432/skillbox_db"
)

users_data = [
    User(name = "Ivan", surname = "Ivanov", email = "Ivanov@mail.ru"),
    User(name = "Petr", surname = "Petrov", email = "Petrov@mail.ru"),
    User(name = "Sidor", surname = "Sidorov", email = "Sidorov@mail.ru")
]

@app.before_request
def startup():
    with Session(engine) as session:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        session.add_all(users_data)
        session.commit()

@app.route('/data')
def get_data_from_db():
    with Session(engine) as session:
        result = session.scalars(select(User))
        users = result.fetchall()
        list_of_users = []
        for user in users:
            list_of_users.append(user.to_json())
        return list_of_users