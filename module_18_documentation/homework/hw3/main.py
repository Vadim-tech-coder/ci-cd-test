import operator

from flasgger import swag_from, Swagger
from flask import Flask
from flask_jsonrpc import JSONRPC

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)


@jsonrpc.method('calc.add')
def add(a: float, b: float) -> float:
    """
    Пример запроса:

    $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
        -d '{
            "jsonrpc": "2.0",
            "method": "calc.add",
            "params": {"a": 7.8, "b": 5.3},
            "id": "1"
        }' http://localhost:5000/api

    Пример ответа:

    HTTP/1.1 200 OK
    Server: Werkzeug/2.2.2 Python/3.10.6
    Date: Fri, 09 Dec 2022 19:00:09 GMT
    Content-Type: application/json
    Content-Length: 54
    Connection: close

    {
      "id": "1",
      "jsonrpc": "2.0",
      "result": 13.1
    }
    """
    return operator.add(a, b)


@jsonrpc.method('calc.sub')
def sub(a: float, b: float) -> float:
    """
        Пример запроса:

        $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
            -d '{
                "jsonrpc": "2.0",
                "method": "calc.sub",
                "params": {"a": 7.8, "b": 5.3},
                "id": "1"
            }' http://localhost:5000/api

        Пример ответа:

        HTTP/1.1 200 OK
        Server: Werkzeug/3.1.3 Python/3.11.9
        Date: Sun, 22 Jun 2025 11:52:54 GMT
        Content-Type: application/json
        Content-Length: 53
        Connection: close

        {
          "id": "1",
          "jsonrpc": "2.0",
          "result": 2.5
        }
    """
    return operator.sub(a, b)


@jsonrpc.method('calc.multiply')
def multiply(a: float, b: float) -> float:
    """
        Пример запроса:

        $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
            -d '{
                "jsonrpc": "2.0",
                "method": "calc.multiply",
                "params": {"a": 7.8, "b": 5.3},
                "id": "1"
            }' http://localhost:5000/api

        Пример ответа:

        HTTP/1.1 200 OK
        Server: Werkzeug/3.1.3 Python/3.11.9
        Date: Sun, 22 Jun 2025 11:54:35 GMT
        Content-Type: application/json
        Content-Length: 68
        Connection: close

        {
          "id": "1",
          "jsonrpc": "2.0",
          "result": 41.339999999999996
        }
    """
    return operator.mul(a, b)


@jsonrpc.method('calc.div')
def divide(a: float, b: float) -> float:
    """
        Пример запроса:

        $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
            -d '{
                "jsonrpc": "2.0",
                "method": "calc.div",
                "params": {"a": 7.8, "b": 5.3},
                "id": "1"
            }' http://localhost:5000/api

        Пример ответа:

        HTTP/1.1 200 OK
        Server: Werkzeug/3.1.3 Python/3.11.9
        Date: Sun, 22 Jun 2025 11:55:51 GMT
        Content-Type: application/json
        Content-Length: 68
        Connection: close

        {
          "id": "1",
          "jsonrpc": "2.0",
          "result": 1.4716981132075473
        }
    """
    try:
        return operator.truediv(a, b)
    except ZeroDivisionError as exc:
        return 0.0

@jsonrpc.method('calc.substract')
def substract(a: float, b: float) -> float:
    """
    This is an endpoint for calculation of result = number1 - number2.
    ---
    tags:
      - calculator
    parameters:
      - in: body
        name: new calculation params
        schema:
          $ref: '#/definitions/Book'
          responses:
            201:
              description: The book has been created
              schema:
              $ref: '#/definitions/Book'
    """
    return operator.sub(a, b)


@jsonrpc.method('calc.multiply')
@swag_from('docs/multiply.yml')
def multiply(a: float, b: float) -> float:
    return operator.mul(a, b)


@jsonrpc.method('calc.divide')
def divide(a: float, b: float) -> float:
    try:
        return operator.truediv(a, b)
    except ZeroDivisionError as exc:
        raise ValueError("Division by zero is not allowed")


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
