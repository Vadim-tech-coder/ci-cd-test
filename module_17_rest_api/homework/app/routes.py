from typing import Tuple, List, Dict

from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import APISpec, Swagger, swag_from
from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError
from werkzeug.serving import WSGIRequestHandler

from models import (
    DATA,
    DATA_AUTHORS,
    get_all_books,
    init_db,
    add_book, get_book_by_id, delete_book_by_id, update_book_by_id, get_all_authors, add_author,
    get_author, delete_books_of_author, get_books_by_author,
)
from schemas import BookSchema, AuthorSchema

app = Flask(__name__)
api = Api(app)


spec = APISpec(
    title='BooksList',
    version='1.0.0',
    openapi_version='2.0',
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin(),
    ],
)

class BookList(Resource):
    @swag_from('get_doc.yml')
    def get(self) -> tuple[list[dict], int]:
        # """
        # This is an endpoint for obtaining the books list.
        # ---
        # tags:
        #   - books
        # responses:
        #   200:
        #     description: Books data
        #     schema:
        #       type: array
        #       items:
        #         $ref: '#/definitions/Book'
        # """
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    @swag_from('post_doc.yml')
    def post(self) -> tuple[dict, int]:
        # """
        # This is an endpoint for book creation.
        # ---
        # tags:
        #  - books
        # parameters:
        #  - in: body
        #    name: new book params
        #    schema:
        #      $ref: '#/definitions/Book'
        # responses:
        #  201:
        #    description: The book has been created
        #    schema:
        #      $ref: '#/definitions/Book'
        #         """
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

specs_dict_get = {
    "description": "This is an endpoint for obtaining the authors list.\nIn this example the specification is taken from dictionary.",
    "tags": ["authors"],
    "responses":{
        "200": {
            "description": "Authors Data",
            "schema": {
                "type": "array",
                "items":{
                    "$ref": "#/definitions/Book"
                        },
                      }
                }
                }
            }


specs_dict_post = {
    "description": "This is an endpoint for creating a new author.\nIn this example the specification is taken from dictionary.",
    "tags": ["authors"],
    "parameters":[
        {
        "in": "body",
        "name": "new author params",
        "description": "Author object to be created",
        "schema": {
            "$ref": "#/definitions/Author"
                    }
        }
                ],
    "responses":{
        "201": {
            "description": "The author has been created",
            "schema": {
                "$ref": "#/definitions/Author"
                        },
                }
            }
        }


class AuthorList(Resource):
    @swag_from(specs_dict_get)
    def get(self) -> tuple[list[dict], int]:
        schema = AuthorSchema()
        return schema.dump(get_all_authors(), many=True), 200

    @swag_from(specs_dict_post)
    def post(self) -> tuple[dict, int]:
        data = request.json
        print(data)
        schema = AuthorSchema()
        try:
            author = schema.load(data)
            print(author)
        except ValidationError as exc:
            return exc.messages, 400

        author = add_author(author)
        return schema.dump(author), 201


api.add_resource(AuthorList, '/api/authors')


class Book(Resource):
    def get(self, book_id: int) -> tuple[list[dict], int]:
        schema = BookSchema()
        return schema.dump(get_book_by_id(book_id)), 200

    def delete(self, book_id: int) -> tuple[dict, int]:
        book = get_book_by_id(book_id)
        if not book:
            return {"message": "Book not found"}, 404

        delete_book_by_id(book_id)
        return {"message": "Book deleted successfully"}, 200

    def patch(self, book_id: int) -> tuple[dict, int]:
        book = get_book_by_id(book_id)
        if not book:
            return {"message": "Book not found"}, 404

        data = request.json
        schema = BookSchema(partial=True) # partial=True разрешает частичное обновление

        try:
            updated_fields = schema.load(data, partial=True)
        except ValidationError as err:
            return err.messages, 400

        # Обновляем поля объекта book
        for key, value in updated_fields.items():
            setattr(book, key, value)

        update_book_by_id(book)  # сохраняем изменения в базе

        return schema.dump(book), 200


api.add_resource(Book, '/api/books/<int:book_id>')



class Author(Resource):
    def get(self, author_id: int) -> tuple[list[dict], int]:
        author = get_author(author_id)
        if not author:
            return {"message": "Author not found"}, 404
        schema = BookSchema()
        return schema.dump(get_books_by_author(author_id),  many=True), 200

    def delete(self, author_id: int) -> tuple[dict, int]:
        author = get_author(author_id)
        if not author:
            return {"message": "Author not found"}, 404

        delete_books_of_author(author_id)
        return {"message": "Books of author were deleted successfully"}, 200


api.add_resource(Author, '/api/authors/<int:author_id>')


template = spec.to_flasgger(
    app,
    definitions=[BookSchema, AuthorSchema],
)

swagger = Swagger(app, template=template)

if __name__ == '__main__':
    init_db(initial_records=DATA, initial_records_of_authors=DATA_AUTHORS)
    app.run(debug=True)
