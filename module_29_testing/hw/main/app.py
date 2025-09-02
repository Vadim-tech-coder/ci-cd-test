from datetime import datetime

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from typing import List

first_request_done = False

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///parking_app.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .models import Client, Parking, ClientParking

    @app.before_request
    def run_once():
        global first_request_done
        if not first_request_done:
            db.create_all()
            first_request_done = True

    # @app.teardown_appcontext
    # def shutdown_session(exception=None):
    #     db.session.remove()

    @app.route("/clients", methods=['POST'])
    def create_client_handler():
        """Создание нового клиента"""
        name = request.form.get('name', type=str)
        surname = request.form.get('surname', type=str)
        credit_card = request.form.get('credit_card', type=str)
        car_number = request.form.get('car_number', type=str)

        new_client = Client(name=name,
                        surname=surname,
                        credit_card=credit_card,
                        car_number=car_number)
        db.session.add(new_client)
        db.session.commit()

        return '', 201


    @app.route("/parkings", methods=['POST'])
    def create_parking_handler():
        """Создание новой парковочной зоны"""
        address = request.form.get('address', type=str)
        opened = request.form.get('opened', type=lambda v: v.lower() == 'true')
        count_places = request.form.get('count_places', type=int)
        count_available_places = request.form.get('count_available_places', type=int)

        new_parking = Parking(address=address,
                            opened=opened,
                            count_places=count_places,
                            count_available_places=count_available_places)

        db.session.add(new_parking)
        db.session.commit()

        return '', 201

    @app.route("/client_parkings", methods=['POST'])
    def create_client_parking_handler():
        """Создание новой записи о заезде на парковку"""
        time_in = datetime.now()
        client_id = request.form.get('client_id', type=int)
        parking_id = request.form.get('parking_id', type=int)

        parking = db.session.get(Parking, parking_id)
        if not parking:
            return jsonify({"error": "Парковка не найдена!"}), 404
        if parking.count_available_places <= 0:
            return jsonify({"error": "На парковке нет свободных мест"}), 400
        if not parking.opened:
            return jsonify({"error": "Парковка закрыта!"}), 404

        new_client_parking = ClientParking(time_in=time_in,
                          client_id=client_id,
                          parking_id=parking_id)

        db.session.add(new_client_parking)

        parking.count_available_places -= 1

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Ошибка при сохранении в БД", "details": str(e)}), 500
        return '', 201

    @app.route("/parkings", methods=['GET'])
    def get_parkings_handler():
        """Получение списка всех парковок"""
        parkings: List[Parking] = db.session.query(Parking).all()
        parkings_list = [p.to_json() for p in parkings]
        return jsonify(parkings_list), 200


    @app.route("/clients", methods=['GET'])
    def get_clients_handler():
        """Получение списка всех клиентов"""
        clients: List[Client] = db.session.query(Client).all()
        clients_list = [c.to_json() for c in clients]
        return jsonify(clients_list), 200

    @app.route("/clients/<int:client_id>", methods=['GET'])
    def get_client_handler(client_id: int):
        """Получение клиента по ид"""
        client: Client = db.session.query(Client).get(client_id)
        return jsonify(client.to_json()), 200

    @app.route("/client_parkings", methods=['DELETE'])
    def delete_client_parking_handler():
        "Удаление записи о парковке клиента по client_id&parking_id"
        client_id = request.args.get('client_id', type=int)
        parking_id = request.args.get('parking_id', type=int)

        if parking_id is None or client_id is None:
            return jsonify({"error": "Не указаны обязательные параметры client_id, parking_id"}), 400

        parking = db.session.get(Parking, parking_id)
        if not parking:
            return jsonify({"error": "Парковка не найдена!"}), 404

        client_parking = db.session.query(ClientParking).filter_by(client_id=client_id,
                                                                   archived_record=False,
                                                                   parking_id = parking_id
                                                                   ).first()
        if not client_parking:
            return jsonify({"error": "Запись о парковке не найдена!"}), 404

        client_card = db.session.get(Client, client_id)
        if client_card is None:
            return jsonify({"error": "Не найдена запись о клиенте!"}), 404
        if client_card.credit_card is None:
            return jsonify({"error": "У клиента нет привязанной карты для оплаты парковки!"}), 404

        client_parking.time_out = datetime.now()
        client_parking.archived_record = True
        parking.count_available_places += 1

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Ошибка при переносе в архив записи!", "details": str(e)}), 500
        return '', 204

    return app
