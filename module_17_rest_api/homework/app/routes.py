from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError

from models import (
    DATA,
    DATA_AUTHORS,
    get_all_books,
    init_db,
    add_book,
)
from schemas import BookSchema

app = Flask(__name__)
api = Api(app)


class BookList(Resource):
    def get(self) -> tuple[list[dict], int]:
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    def post(self) -> tuple[dict, int]:
        data = request.json
        print(data)
        schema = BookSchema()
        try:
            book = schema.load(data)
            print(book)
        except ValidationError as exc:
            return exc.messages, 400

        book = add_book(book)
        return schema.dump(book), 201


api.add_resource(BookList, '/api/books')

if __name__ == '__main__':
    init_db(initial_records=DATA, initial_records_of_authors=DATA_AUTHORS)
    app.run(debug=True)
