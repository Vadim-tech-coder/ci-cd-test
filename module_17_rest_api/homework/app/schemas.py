from typing import Required

from marshmallow import Schema, fields, validates, ValidationError, post_load

from models import get_book_by_title, Book, Author


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author_id = fields.Int(required=True)

    @validates('title')
    def validate_title(self, title: str, **kwargs) -> None:
        print(f"Validating title: {title}")
        if get_book_by_title(title) is not None:
            raise ValidationError(
                f'Book with title "{title}" already exists, '
                'please use a different title.'
            )

    @post_load
    def create_book(self, data: dict, **kwargs):
        if self.partial:
            return data
        return Book(**data)


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    middle_name = fields.Str()

    @post_load
    def create_author(self, data: dict, **kwargs):
        return Author(**data)