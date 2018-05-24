from flask_restful import Resource
from flask import json, request, Response
from api.models import Book


class Books(Resource):
    def post(self):
        data = request.get_json(self)
        if len(data) == 0:
            return Response(json.dumps({"Message": "Book information not passed"}), status=403)
        data['title'] = data['title'].strip().lower().title()
        data['author'] = data['author'].strip()
        data['isbn'] = data['isbn'].strip()
        data['publisher'] = data['publisher'].strip()
        data['quantity'] = data['quantity']
        if not data['title']:
            return Response(json.dumps({"Message": "Book title not provided"}), status=403)
        if not data['author']:
            return Response(json.dumps({"Message": "Book author not provided"}), status=403)
        if not data['isbn']:
            return Response(json.dumps({"Message": "Book isbn not provided"}), status=403)
        if not data['publisher']:
            return Response(json.dumps({"Message": "Book publisher not provided"}), status=403)
        if not data['quantity']:
            return Response(json.dumps({"Message": "Book quantity not provided"}), status=403)
        Book(data['title'], data['author'], data['isbn'], data['publisher'], data['quantity']).save()
        return Response(json.dumps({"Message": "Book added successfully"}), status=201)

    def get(self):
        books = Book.all_books()
        if len(books) == 0:
            return Response(json.dumps({"Message": "No books found"}), status=404)
        return Response(json.dumps({"Books": [book.serialize for book in books]}), status=200)