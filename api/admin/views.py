from api import jwt
from api.models import Book, User
from flask_restful import Resource
from flask import json, request, Response
from flask_jwt_extended import get_jwt_identity, jwt_required


class AddBook(Resource):
    """[summary]
    
    Arguments:
        Resource {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)
        if user:
            if user.is_admin:
                data = request.get_json(self)
                if len(data) == 0:
                    return Response(json.dumps({"Message": "Book information not passed"}), status=403)
                data['title'] = data['title'].strip().lower().title()
                data['author'] = data['author'].strip().title()
                data['isbn'] = data['isbn'].strip()
                data['publisher'] = data['publisher'].strip().title()
                if not data['title']:
                    return Response(json.dumps({"Message": "Book title not provided"}), status=403)
                if len(data['title']) > 500:
                    return Response(json.dumps({"Message": "Title exceeds 500 character limit"}), status=403)
                if not data['author']:
                    return Response(json.dumps({"Message": "Book author not provided"}), status=403)
                if len(data['author']) > 100:
                    return Response(json.dumps({"Message": "Author exceeds 100 character limit"}), status=403)
                if not data['isbn']:
                    return Response(json.dumps({"Message": "Book isbn not provided"}), status=403)
                if len(data['isbn']) > 100:
                    return Response(json.dumps({"Message": "ISBN exceeds 100 character limit"}), status=403)
                if not data['publisher']:
                    return Response(json.dumps({"Message": "Book publisher not provided"}), status=403)
                if len(data['publisher']) > 100:
                    return Response(json.dumps({"Message": "Publisher exceeds 100 character limit"}), status=403)
                if not data['quantity']:
                    return Response(json.dumps({"Message": "Book quantity not provided"}), status=403)
                books = Book.get_all_books()
                isbn = [book for book in books if book.isbn == data['isbn']]
                if isbn:
                    return Response(json.dumps({"Message": "Book already exists"}), status=409)
                Book(data['title'], data['author'], data['isbn'], data['publisher'], data['quantity']).save()
                return Response(json.dumps({"Message": "Book added successfully"}), status=201)
            return Response(json.dumps({"Message": "User not an admin"}), status=401)
        return Response(json.dumps({"Message": "User does not exist"}), status=404)


class BookOps(Resource):
    """[summary]
    
    Arguments:
        Resource {[type]} -- [description]
    """
    @jwt_required
    def put(self, book_id):
        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)
        if user:
            if user.is_admin:
                try:
                    book_id = int(book_id)
                except Exception as e:
                    return Response(json.dumps({"Message": "Invalid argument passed"}), status=400)
                book = Book.get_book_by_id(book_id)
                if book:
                    data = request.get_json(self)
                    if len(data) == 0:
                        return Response(json.dumps({"Message": "Book information not passed"}), status=400)
                    data['title'] = data['title'].strip().lower().title()
                    data['author'] = data['author'].strip().title()
                    data['isbn'] = data['isbn'].strip()
                    data['publisher'] = data['publisher'].strip().title()
                    if not data['title']:
                        return Response(json.dumps({"Message": "Book title not provided"}), status=403)
                    if len(data['title']) > 500:
                        return Response(json.dumps({"Message": "Title exceeds 100 character limit"}), status=403)
                    if not data['author']:
                        return Response(json.dumps({"Message": "Book author not provided"}), status=403)
                    if len(data['author']) > 100:
                        return Response(json.dumps({"Message": "Author exceeds 100 character limit"}), status=403)
                    if not data['isbn']:
                        return Response(json.dumps({"Message": "Book isbn not provided"}), status=403)
                    if len(data['isbn']) > 100:
                        return Response(json.dumps({"Message": "ISBN exceeds 100 character limit"}), status=403)
                    if not data['publisher']:
                        return Response(json.dumps({"Message": "Book publisher not provided"}), status=403)
                    if len(data['publisher']) > 100:
                        return Response(json.dumps({"Message": "Publisher exceeds 100 character limit"}), status=403)
                    if not data['quantity']:
                        return Response(json.dumps({"Message": "Book quantity not provided"}), status=403)
                    book.title = data['title']
                    book.author = data['author']
                    book.isbn = data['isbn']
                    book.publisher = data['publisher']
                    book.quantity = data['quantity']
                    book.save()
                    return Response(json.dumps({"Message": "Book updated successfully"}), status=200)
                return Response(json.dumps({"Message": "Book does not exist"}), status=404)
            return Response(json.dumps({"Message": "User not an admin"}), status=401)
        return Response(json.dumps({"Message": "User does not exist"}), status=404)
    
    @jwt_required
    def delete(self, book_id):
        """[summary]
        
        Arguments:
            book_id {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)
        if user:
            if user.is_admin:
                book = Book.get_book_by_id(book_id)
                if book:
                    book.delete()
                    return Response(json.dumps({"Message": "Book deleted successfully"}), status=200)
                return Response(json.dumps({"Message": "Book doesn't exist"}), status=404)
            return Response(json.dumps({"Message": "User not an admin"}), status=401)
        return Response(json.dumps({"Message": "User does not exist"}), status=404)    
