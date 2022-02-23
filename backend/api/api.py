from flask import Blueprint
from flask_restful import Api

from api.resources.book import BookCollection, BookItem

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

api.add_resource(BookCollection, "/books/")
api.add_resource(BookItem, "/books/<book_id>/")
