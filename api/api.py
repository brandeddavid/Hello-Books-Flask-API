from flask_restful import Resource
from api.models import *
from flask import jsonify, request

b1 = Book('The Lean Start Up', 'Eric Ries', '12345').createbook()
b2 = Book('A Game of Thrones', 'George R.R. Martin', '67890').createbook()
b2 = Book('If Tomorrow Comes', 'Sidney Sheldon', '54321').createbook()


class GetAllBooks(Resource):
    """"
    """
    def post(self):

        pass

    def get(self):

        return Book.get_all_books()


class BookOps(Resource):

    def get(self, book_id):

        return jsonify(Book.getbook(id=book_id))

    def put(self, book_id):

        data = request.get_json(self)

        return jsonify(Book.updatebook(id=book_id, data=data))

    def delete(self, book_id):

        return jsonify(Book.deletebook(id=book_id))

    def post(self, book_id):

        data = request.get_json(self)

        return jsonify(Book.apicreatebook(id=book_id, data=data))
