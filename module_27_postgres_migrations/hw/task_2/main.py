import json

import requests
from flask import Flask, request
from models import Base, User, Coffee
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, update
import random
from sqlalchemy import func

app = Flask(__name__)
engine = create_engine(
    "postgresql+psycopg2://skillbox:skillbox@localhost:5432/skillbox_db", echo=True
)

first_request = True

@app.before_request
def startup():
    global first_request
    if first_request:
        with Session(engine) as session:
            Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)
            fetch_coffee_and_save(10)
            fetch_users_and_save(10)
            session.commit()
        first_request = False

@app.route('/')
def hello_world():
    return 'Hello, World!'


def fetch_users_and_save(quantity=10):
    url = f"https://fakerapi.it/api/v1/persons?_quantity={quantity}"
    response = requests.get(url)
    data = response.json()["data"]
    with Session(engine) as session:
        for item in data:
            user = User(
                name=item["firstname"] + " " + item["lastname"],
                has_sale=random.randint(0,1),
                address={
                    "street": item["address"]["street"],
                    "city": item["address"]["city"],
                    "country": item["address"]["country"]
                },
                coffee_id=random.randint(1,10),
            )
            session.add(user)
            session.execute(
                update(User)
                .values(search_vector=func.to_tsvector('english', User.address))
            )
        session.commit()


def fetch_coffee_and_save(quantity=10):
    url = f"https://fakerapi.it/api/v1/companies?_quantity={quantity}"
    response = requests.get(url)
    data = response.json()["data"]
    with Session(engine) as session:
        for item in data:
            coffee = Coffee(
                title=item["name"],
                category=item["country"],
                description=item["addresses"][0]["streetName"],
                reviews=[item["website"], item["image"], item["email"]],
            )
            session.add(coffee)
            session.execute(
                update(Coffee)
                .values(search_vector=func.to_tsvector('english', Coffee.title))
            )
        session.commit()


@app.route("/add_user", methods = ['POST'])
def add_user():
    user_data = request.json
    user = User(
        name = user_data['name'], address = user_data['address'],
        has_sale=int(user_data['has_sale']), coffee_id=int(user_data['coffee_id'])
    )
    with Session(engine) as session:
        session.add(user)
        session.flush()
        data = user.to_json()
        data['coffee_id']=user.coffee_id
        session.commit()
        return data

@app.route("/search", methods = ['POST'])
def search_coffee_by_title():
    search_string = request.json['search_string']
    with Session(engine) as session:
        query = session.execute(select(Coffee).where(Coffee.title.match(search_string)))
        coffee = query.scalars().all()
        search_result = []
        for c in coffee:
            search_result.append(c.to_json())
    return search_result


@app.route("/unique")
def get_unique_reviews():
    with Session(engine) as session:
        unique_reviews = session.query(func.unnest(Coffee.reviews)).distinct().all()
        data = {}
        for review in unique_reviews:
            data["unique_list_review"] = data.get("unique_list_review", []) + [review[0]]
        data["quantity_reviews"] = len(unique_reviews)
        return data


@app.route("/users_from", methods=["POST"])
def get_list_of_users_from_country():

    country = request.json['country']
    with Session(engine) as session:
        result = session.execute(
            select(User).where(User.address["country"].astext.match(country))
        ).scalars().all()
        list_users = []
        for u in result:
            list_users.append(u.to_json())
    return list_users