import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker

from main.app import db
from main.models import Client, Parking

fake = Faker()

class ClientFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    name = factory.LazyAttribute(lambda x: fake.first_name())
    surname = factory.LazyAttribute(lambda x: fake.last_name())
    credit_card = factory.LazyAttribute(lambda x: fake.credit_card_number())
    car_number = factory.LazyAttribute(lambda x: fake.license_plate())

class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    address = factory.LazyAttribute(lambda x: fake.address())
    opened = factory.LazyAttribute(lambda x: fake.boolean(chance_of_getting_true=50))
    count_places = factory.LazyAttribute(lambda x: fake.random_int(min=5, max=100))
    count_available_places = factory.LazyAttribute(lambda x: fake.random_int(min=0, max=50))