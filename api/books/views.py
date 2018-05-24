from flask_restful import Resource
from flask import json, request, Response
from api.models import Book


class Books(Resource):
    def post(self):
        data = request.get_json(self)
        if len(data) == 0:
            return Response(json.dumps({"Message": "Book information not passed"}), status=403)
        data['title'] = data['title'].strip().lower().title()
        data['author'] = data['author'].strip().title()
        data['isbn'] = data['isbn'].strip()
        data['publisher'] = data['publisher'].strip().title()
        data['quantity'] = data['quantity']
        if not data['title']:
            return Response(json.dumps({"Message": "Book title not provided"}), status=403)
        if len(data['title']) > 500:
            return Response(json.dumps({"Message": "Title exceeds 500 character limit"}), status=403)
        if not data['author']:
            return Response(json.dumps({"Message": "Book author not provided"}), status=403)
        if len(data['author']) > 100:
            return Response(json.dumps({"Message": "Author exceeds 500 character limit"}), status=403)
        if not data['isbn']:
            return Response(json.dumps({"Message": "Book isbn not provided"}), status=403)
        if len(data['isbn']) > 100:
            return Response(json.dumps({"Message": "ISBN exceeds 500 character limit"}), status=403)
        if not data['publisher']:
            return Response(json.dumps({"Message": "Book publisher not provided"}), status=403)
        if len(data['publisher']) > 100:
            return Response(json.dumps({"Message": "Publisher exceeds 500 character limit"}), status=403)
        if not data['quantity']:
            return Response(json.dumps({"Message": "Book quantity not provided"}), status=403)
        books = Book.all_books()
        isbn = [book for book in books if book.isbn == data['isbn']]
        if isbn:
            return Response(json.dumps({"Message": "Book already exists"}), status=403)
        Book(data['title'], data['author'], data['isbn'], data['publisher'], data['quantity']).save()
        return Response(json.dumps({"Message": "Book added successfully"}), status=201)

    def get(self):
        books = Book.all_books()
        if len(books) == 0:
            return Response(json.dumps({"Message": "No books found"}), status=404)
        return Response(json.dumps({"Books": [book.serialize for book in books]}), status=200)


class BookOps(Resource):
    """[summary]
    
    Arguments:
        Resource {[type]} -- [description]
    """
    def get(self, book_id):
        try:
            book_id = int(book_id)
        except Exception as e:
            return Response(json.dumps({"Message": "Invalid argument passed"}))
        book = Book.book_by_id(id=book_id)
        if not book:
            return Response(json.dumps({"Message": "Book does not exist"}), status=404)
        return Response(json.dumps(book.serialize), status=200)

    def put(self, book_id):
        pass
    
    def delete(self, book_id):
        pass

