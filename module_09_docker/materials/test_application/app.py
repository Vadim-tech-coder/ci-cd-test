import os
import getpass

from flask import Flask, jsonify, make_response

DEVELOPER = getpass.getuser()
APP = Flask(__name__)
HOST = '0.0.0.0'
PORT = 5000
SERVICE_NAME = os.environ.get('SERVICE_NAME', 'application')


@APP.route('/hello/<user>')
def hello_user(user: str):
    return make_response(
        jsonify(
            {'message': f'Hello from {SERVICE_NAME}, {user}!\nIn case of any trouble contact {DEVELOPER}'}
        ),
        200
    )


if __name__ == '__main__':
    APP.run(host=HOST, port=PORT)
