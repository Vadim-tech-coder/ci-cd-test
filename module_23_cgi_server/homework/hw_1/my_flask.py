import json
import re
from wsgiref.simple_server import make_server


class MyFlask:

    def __init__(self):
        self.routes = {}


    def route(self, path):

        def wrapper(func):
            count = re.search(r'(<)', path)
            endpoint = path[:count.start()] if count is not None else path
            self.routes[endpoint] = func
            return func
        return wrapper


    def __call__(self, environ, start_response):
        self.environ = environ
        path = self.environ.get('PATH_INFO')
        headers = [('Content-type', 'application/json')]


        if path == '/hello':
            status = '200 OK'
            response = self.routes[path]()
            start_response(status, headers)
            return [json.dumps(response).encode('utf-8')]
        elif path.startswith('/hello'):
            status = '200 OK'
            query = path.split('/')[2]
            response = self.routes['/hello/'](query)
            start_response(status, headers)
            return [json.dumps(response).encode('utf-8')]
        else:
            status = '404 Not Found'
            response = {'error': 'Not found'}
            start_response(status, headers)
            return [json.dumps(response).encode('utf-8')]


application = MyFlask()

@application.route('/hello')
def hello_world():
    return {"response": "Hello, World!"}

@application.route('/hello/<username>')
def hello_user(username):
    return {"response": f"Hello, {username}!"}

if __name__ == '__main__':
    server = make_server(host = '0.0.0.0', port=5000, app=application)
    print(f"Сервер {application.__class__} запущен!")
    server.serve_forever()