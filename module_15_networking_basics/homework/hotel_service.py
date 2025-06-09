from flask import Flask, request, jsonify

app: Flask = Flask(__name__)

rooms = [
    {"roomId": 1, "floor": 2, "guestNum": 1, "beds": 1, "price": 2000},
    {"roomId": 2, "floor": 1, "guestNum": 2, "beds": 1, "price": 2500}
    ]

@app.route('/rooms', methods = ['post',])
def add_room():
    """Функция для эндпоинта для добавления номера."""
    try:
        new_room_id = len(rooms) + 1
        data = request.json
        new_room = {"roomId": new_room_id, "floor": data["floor"], "guestNum": data["guestNum"],
                    "beds": data["beds"], "price": data["price"]}
        rooms.append(new_room)
        print(rooms)
        return jsonify(sucess=True), 200
    except Exception as err:
        return jsonify(error = str(err)), 500


@app.route('/rooms', methods = ['get',])
def get_room():
    """Функция для эндпоинта для получение списка всех номеров."""
    try:
        return jsonify({'rooms': rooms}), 200
    except Exception as err:
        return jsonify(error = str(err)), 500



@app.route('/bookings', methods = ['post',])
def book_room():
    """Функция для эндпоинта для бронирования номера, удаляет забронированный номер."""
    try:
        data = request.json
        room_id = data.get('roomId')
        print(room_id)
        for room in rooms:
            # print(rooms)
            if room.get("roomId") == room_id:
                response = jsonify(success=True, booked_room = {"roomId": room["roomId"], "floor": room["floor"],
                                                            "guestNum": room["guestNum"], "beds": room["beds"],
                                                            "price": room["price"]}), 200
                rooms.remove(room)
                return response
        else:
            return jsonify(error="Room not Found"), 409
    except Exception as err:
        return jsonify(error = str(err)), 500

if __name__ == '__main__':
    app.run(debug=True)