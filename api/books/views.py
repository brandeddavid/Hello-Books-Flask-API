from flask_restful import Resource
from flask import json, request, Response
from api.models import Book


class GetBooks(Resource):
    """[summary]
    
    Arguments:
        Resource {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """    
    def get(self):
        books = Book.get_all_books()
        if len(books) == 0:
            return Response(json.dumps({"Message": "No books found"}), status=404)
        return Response(json.dumps({"Books": [book.serialize for book in books]}), status=200)


class GetBook(Resource):
    """[summary]
    
    Arguments:
        Resource {[type]} -- [description]
    """
    def get(self, book_id):
        try:
            book_id = int(book_id)
        except Exception as e:
            return Response(json.dumps({"Message": "Invalid argument passed"}), status=403)
        book = Book.get_book_by_id(id=book_id)
        if not book:
            return Response(json.dumps({"Message": "Book does not exist"}), status=404)
        return Response(json.dumps(book.serialize), status=200)
