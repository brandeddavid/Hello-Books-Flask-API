"""File has admin endpoints resources"""

from api import jwt
from api.models import Book, User
from api.validate import validate_book, validate_arg
from flask_restful import Resource
from flask import json, request, Response
from flask_jwt_extended import get_jwt_identity, jwt_required


class AddBook(Resource):
   """Add Book API endpoint Resource"""
    
    @jwt_required
    def post(self):
        """Method serving add book api endpoint"""
        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)
        if user:
            if user.is_admin:
                data = request.get_json(self)
                if validate_book(data):
                    return validate_book(data)
                books = Book.get_all_books()
                isbn = [book for book in books if book.isbn == data['isbn']]
                if isbn:
                    return Response(json.dumps({"Message": "Book already exists"}), status=409)
                Book(data['title'], data['author'], data['isbn'], data['publisher'], data['quantity']).save()
                return Response(json.dumps({"Message": "Book added successfully"}), status=201)
            return Response(json.dumps({"Message": "User not an admin"}), status=401)
        return Response(json.dumps({"Message": "User does not exist"}), status=404)


class BookOps(Resource):
    """BookOps (Edit and Delete) Resource"""

    @jwt_required
    def put(self, book_id):
        """Function serving edit book api endpoint"""
        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)
        if validate_arg(book_id):
            return validate_arg(book_id)
        if user:
            if user.is_admin:
                book = Book.get_book_by_id(book_id)
                if book:
                    data = request.get_json(self)
                    if validate_book(data):
                        return validate_book(data)
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
        """Function serving delete book api endpoint"""
        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)
        if validate_arg(book_id):
            return validate_arg(book_id)
        if user:
            if user.is_admin:
                book = Book.get_book_by_id(book_id)
                if book:
                    book.delete()
                    return Response(json.dumps({"Message": "Book deleted successfully"}), status=200)
                return Response(json.dumps({"Message": "Book doesn't exist"}), status=404)
            return Response(json.dumps({"Message": "User not an admin"}), status=401)
        return Response(json.dumps({"Message": "User does not exist"}), status=404)


class PromoteUser(Resource):
    """Promote user resource"""

    @jwt_required
    def post(self):
       """Function serving promote user api endpoint"""
        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)
        if user:
            if user.is_admin:
                data = request.get_json(self)
                User.promote_user(data['username'].lower())
                return Response(json.dumps({"Message": "User promoted successfully"}), status=200)
            return Response(json.dumps({"Message": "User not an admin"}), status=401)
        return Response(json.dumps({"Message": "User does not exist"}), status=404)   
        data = request.get_json(self)
        User.promote_user(data['username'])
        return Response(json.dumps({"Message": "User promoted successfully"}), status=200)
