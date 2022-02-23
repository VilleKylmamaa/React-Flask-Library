import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from api.models import Book
from api import db
from api.utils import LibraryBuilder, create_error_response

MASON = "application/vnd.mason+json"


class BookCollection(Resource):

    def get(self):
        body = LibraryBuilder()
        body.add_namespace("library", "n/a")
        body.add_control("self", url_for("api.bookcollection"))
        body.add_control_add_book()
        
        body["items"] = []
        for db_book in Book.query.all():
            item = LibraryBuilder(
                book_id=db_book.book_id,
                title=db_book.title,
                author=db_book.author,
                description=db_book.description
            )
            item.add_control("self", url_for(
                "api.bookitem", 
                book_id=db_book.book_id
                )
            )
            item.add_control_edit_book(db_book.book_id)
            item.add_control_delete_book(db_book.book_id)
            body["items"].append(item)

        return Response(json.dumps(body, indent=4, default=str), 200, mimetype=MASON)


    def post(self):
        if not request.json:
            return create_error_response(
                415, "Unsupported media type", "Requests must be JSON"
            )

        try:
            validate(request.json, Book.get_schema())
        except ValidationError as e:
            return create_error_response(400,
                "Invalid JSON document. Missing field or incorrect type.", str(e)
            )

        book = Book(
            title=request.json["title"],
            author=request.json["author"],
            description=request.json["description"]
        )

        db.session.add(book)
        db.session.commit()

        return Response(status=201, headers={
            "Location": url_for("api.bookitem", book_id=book.book_id)
        })



class BookItem(Resource):
    
    def get(self, book_id):
        db_book = Book.query.filter_by(book_id=book_id).first()
        if db_book is None:
            return create_error_response(
                404, "Not found",
                "No book was found with the id '{}'".format(book_id)
            )

        
        if db_book is not None:
            body = LibraryBuilder(
                book_id=db_book.book_id,
                title=db_book.title,
                author=db_book.author,
                description=db_book.description
            )
            body.add_namespace("library", "n/a")
            body.add_control("self", url_for("api.bookitem", book_id=book_id))
            body.add_control("collection", url_for("api.bookcollection"))
            body.add_control_edit_book(book_id)
            body.add_control_delete_book(book_id)
            
        return Response(json.dumps(body, indent=4), 200, mimetype=MASON)


    def put(self, book_id):
        db_book = Book.query.filter_by(book_id=book_id).first()
        if db_book is None:
            return create_error_response(
                404, "Not found",
                "No book was found with the id '{}'".format(book_id)
            )

        if not request.json:
            return create_error_response(
                415, "Unsupported media type",
                "Requests must be JSON"
            )

        try:
            validate(request.json, Book.get_schema())
        except ValidationError as e:
            return create_error_response(400,
                "Invalid JSON document. Missing field or incorrect type.", str(e)
            )
            
        db_book.title = request.json["title"]
        db_book.author = request.json["author"]
        db_book.description = request.json["description"]
        db.session.commit()

        return Response(status=204, headers={
            "Location": url_for("api.bookitem", book_id=db_book.book_id)
        })
        

    def delete(self, book_id):
        db_book = Book.query.filter_by(book_id=book_id).first()
        if db_book is None:
            return create_error_response(
                404, "Not found",
                "No book was found with the id '{}'".format(book_id)
            )

        db.session.delete(db_book)
        db.session.commit()

        return Response(status=204)