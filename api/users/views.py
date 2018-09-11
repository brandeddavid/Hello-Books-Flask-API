"""File containing user api endpoints resources"""

from api.models import User, Book, BorrowBook
from api.admin.validate import validate_arg
from flask_restful import Resource, reqparse
from flask import request, json, Response
from flask_jwt_extended import get_jwt_identity, jwt_required
from datetime import datetime

parser = reqparse.RequestParser()


class GetAllUsers(Resource):
    """Get all users resource"""

    @jwt_required
    def get(self):
        """Function serving get all user api endpoint"""
        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)
        if user:
            if user.is_admin:
                allUsers = User.all_users()
                if len(allUsers) == 0:
                    return Response(json.dumps({"Message": "No users found"}), status=404)
                return Response(json.dumps({"Users": [user.serialize for user in allUsers]}), status=200)
            return Response(json.dumps({"Message": "User not an admin"}), status=401)
        return Response(json.dumps({"Message": "User does not exist"}), status=404)


class GetUser(Resource):
    """Get one user resource"""

    @jwt_required
    def get(self):
        """Function serving get all user api endpoint"""
        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)
        if user:
            return Response(json.dumps({"User": user.serialize}), status=200)
        return Response(json.dumps({"Message": "User does not exist"}), status=404)
        

class BorrowOps(Resource):
    """Borrow book ops (Borrow and Return) resource"""

    @jwt_required
    def post(self, book_id):
        """Function serving borrow book api endpoint"""
        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)
        if user:
            if validate_arg(book_id):
                return Response(json.dumps(validate_book(data)), status=400)
            book = Book.get_book_by_id(book_id)
            if book:
                if book.quantity == 0:
                    return Response(json.dumps({"Message": "Book not available to borrow"}), status=404)
                borrowed = BorrowBook.query.filter_by(user_id=user.id, book_id=book.id, returned=False).first()
                if borrowed:
                    return Response(json.dumps({"Message": "Already borrowed book"}), status=403)
                BorrowBook(user=user, book=book).save()
                book.quantity -= 1
                book.save()
                return Response(json.dumps({"Message": "Book borrowed successfully", "Book": book.serialize}), status=200)
            return Response(json.dumps({"Message": "Book does not exist"}), status=404)
        return Response(json.dumps({"Message": "User does not not exist"}), status=404)

    @jwt_required
    def put(self, book_id):
        """Function serving return book api endpoint"""
        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)
        if user:
            if validate_arg(book_id):
                return Response(json.dumps(validate_book(data)), status=403)
            book = Book.get_book_by_id(book_id)
            if book:
                to_return = BorrowBook.query.filter_by(user_id=user.id, book_id=book.id, returned=False).first()
                if to_return:
                    to_return.returned = True
                    to_return.date_returned = datetime.now()
                    to_return.save()
                    book.quantity += 1
                    book.save()
                    return Response(json.dumps({"Message": "Book returned successfully"}), status=200)
                return Response(json.dumps({"Message": "You had not borrowed this book"}), status=403)
            return Response(json.dumps({"Message": "Book does not exist"}), status=404)
        return Response(json.dumps({"Message": "User does not exist"}), status=404)


class BorrowHistory(Resource):
    """Borrowing History api endpoint resource"""

    @jwt_required
    def get(self):
        """Function serving get user borrowing history api endpoint"""
        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)
        if user:
            args = parser.parse_args()
            returned = request.args.get('returned')
            if returned == 'false':
                unreturned_books = BorrowBook.get_books_not_returned(user.id)
                if unreturned_books:
                    return Response(json.dumps({"unreturned": unreturned_books}), status=200)
                return Response(json.dumps({"Message": "You do not have any unreturned book"}), status=403)
            borrow_history = BorrowBook.get_user_borrowing_history(user.id)
            if borrow_history:
                return Response(json.dumps({"borrowHistory": borrow_history}), status=200)
            return Response(json.dumps({"Message": "You have not borrowed any book"}), status=404)
        return Response(json.dumps({"Message": "User does not exist"}), status=404)
