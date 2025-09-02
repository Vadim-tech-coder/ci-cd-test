import pytest
from datetime import datetime, timedelta

from main.app import create_app, db
from main.models import Client, ClientParking, Parking


@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config.update(
        {
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
        }
    )
    with app.app_context():
        db.create_all()

        client = Client(name = 'Test', surname = 'User',
                        credit_card = '4565213254659887', car_number = 'A480VF174')
        parking = Parking(address = 'Test Address 174/3', opened = True,
                           count_places = 10, count_available_places = 10)
        db.session.add_all([client, parking])


        time_in = datetime.now() - timedelta(hours=1)
        time_out = datetime.now()
        client_parking = ClientParking(client_id = client.id, parking_id = parking.id,
                                       time_in = time_in, time_out = time_out,
                                       archived_record = True)
        db.session.add(client_parking)
        parking.count_available_places -= 1
        db.session.commit()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture(scope='module')
def _db(app):
    with app.app_context():
        yield db
