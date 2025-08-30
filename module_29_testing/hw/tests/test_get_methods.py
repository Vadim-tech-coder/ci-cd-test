import pytest
from datetime import datetime

@pytest.mark.parametrize("url", [
    "/clients",
    "/parkings",
])
def test_get_endpoints_return_200(client, url):
    response = client.get(url)
    assert response.status_code == 200


def test_create_client(client, _db):
    data = {
        "name": "John",
        "surname": "Doe",
        "credit_card": "1234567890123456",
        "car_number": "XYZ123"
    }
    response = client.post("/clients", data=data)
    assert response.status_code == 201

    # Проверка что клиент создан в БД
    from main.models import Client  # Импорт модели Client
    created_client = _db.session.query(Client).filter_by(name="John", surname="Doe").first()
    assert created_client is not None
    assert created_client.credit_card == data["credit_card"]


def test_create_parking(client, _db):
    data = {
        "address": "Test St, 1",
        "opened": "true",
        "count_places": "10",
        "count_available_places": "10"
    }
    response = client.post("/parkings", data=data)
    assert response.status_code == 201

    from main.models import Parking
    created_parking = _db.session.query(Parking).filter_by(address="Test St, 1").first()
    assert created_parking is not None
    assert created_parking.opened is True
    assert created_parking.count_places == 10


@pytest.mark.parking
def test_parking_entry(client, _db):
    from main.models import Client, Parking, ClientParking

    client_obj = _db.session.query(Client).filter(Client.credit_card.isnot(None)).first()
    parking_obj = _db.session.query(Parking).filter(
        Parking.opened == True, Parking.count_available_places > 0).first()

    old_available = parking_obj.count_available_places

    data = {
        "client_id": client_obj.id,
        "parking_id": parking_obj.id
    }
    response = client.post("/client_parkings", data=data)
    assert response.status_code == 201

    _db.session.refresh(parking_obj)
    assert parking_obj.count_available_places == old_available - 1

    # Убедиться, что создана запись въезда
    client_parking = _db.session.query(ClientParking).filter_by(
        client_id=client_obj.id,
        parking_id=parking_obj.id,
        archived_record=False
    ).first()
    assert client_parking is not None
    assert client_parking.time_in is not None


@pytest.mark.parking
def test_parking_exit(client, _db):
    from main.models import ClientParking, Parking

    client_parking = _db.session.query(ClientParking).filter_by(archived_record=False).first()
    parking_obj = _db.session.get(Parking, client_parking.parking_id)

    old_available = parking_obj.count_available_places

    data = {
        "client_id": client_parking.client_id,
        "parking_id": client_parking.parking_id
    }
    response = client.delete("/client_parkings", query_string=data)
    assert response.status_code == 204

    _db.session.refresh(parking_obj)
    _db.session.refresh(client_parking)

    assert parking_obj.count_available_places == old_available + 1
    assert client_parking.archived_record == True
    assert client_parking.time_out is not None
    assert client_parking.time_out >= client_parking.time_in

    # Проверить, что у клиента есть карта
    client_obj = client_parking.client
    assert client_obj.credit_card is not None
