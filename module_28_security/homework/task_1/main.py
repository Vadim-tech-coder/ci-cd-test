from flask import Flask, jsonify, request, Response

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_handler():
    print(request.headers)
    return jsonify({"Hello from GET": "User"})

@app.route('/', methods=['POST'])
def post_handler():
    print(request.headers)
    return jsonify({"Hello from POST": "User"})

@app.route('/', methods=['PUT'])
def put_handler():
    print(request.headers)
    return jsonify({"Hello from PUT": "User"})

@app.after_request
def add_cors(response: Response):
    response.headers['Access-Control-Allow-Origin'] = 'https://www.google.com'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'X-My-Fancy-Header'
    return response


if __name__ == '__main__':
    app.run(port=8080, debug=True)
