from api.models import User, Book, BorrowBook
from flask_restful import Resource
from flask import request, json, Response
from flask_jwt_extended import get_jwt_identity, jwt_required
from datetime import datetime


class GetAllUsers(Resource):
    """[summary]
    
    Arguments:
        Resource {[type]} -- [description]
    """
    def get(self):
        allUsers = User.all_users()
        if len(allUsers) == 0:
            return Response(json.dumps({"Message":"No users found"}))
        return Response(json.dumps({"Users":[user.serialize for user in allUsers]}))

class BorrowOps(Resource):
    """[summary]
    
    Arguments:
        Resource {[type]} -- [description]
    """

    @jwt_required
    def post(self, book_id):
        """[summary]
        
        Arguments:
            book_id {[type]} -- [description]
        """
        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)
        if user:
            try:
                book_id = int(book_id)
            except:
                return Response(json.dumps({"Message": "Invalid argument passed"}), status=403)
            book = Book.get_book_by_id(book_id)
            if book:
                if book.quantity == 0:
                    return Response(json.dumps({"Message": "Book not available to borrow"}), status=404)
                borrowed_books = BorrowBook.get_all_borrowed_books()
                borrowed = [borrowed_book for borrowed_book in borrowed_books if borrowed_book.user_id == user.id and borrowed_book.book_id == book.id and borrowed_book.returned == False]
                if borrowed:
                    return Response(json.dumps({"Message": "Already borrowed book"}), status=403)
                BorrowBook(user=user, book=book).save()
                book.quantity -= 1
                book.save()
                return Response(json.dumps({"Message": "Book borrowed successfully"}), status=200)
            return Response(json.dumps({"Message": "Book does not exist"}), status=404)
        return Response(json.dumps({"Message": "User does not not exist"}), status=404)

    @jwt_required
    def put(self, book_id):
        """[summary]
        
        Arguments:
            book_id {[type]} -- [description]
        """
        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)
        if user:
            try:
                book_id = int(book_id)
            except:
                return Response(json.dumps({"Message": "Invalid argument passed"}), status=403)
            book = Book.get_book_by_id(book_id)
            if book:
                borrowed_books = BorrowBook.get_all_borrowed_books()
                to_return = [borrowed_book for borrowed_book in borrowed_books if borrowed_book.book_id == book_id and borrowed_book.returned ==False]
                if to_return:
                    to_return[0].returned = True
                    to_return[0].date_returned = datetime.now()
                    to_return[0].save()
                    book.quantity += 1
                    book.save()
                    return Response(json.dumps({"Message": "Book returned successfully"}), status=200)
                return Response(json.dumps({"Message": "You had not borrowed this book"}), status=403)
            return Response(json.dumps({"Message": "Book does not exist"}), status=404)
        return Response(json.dumps({"Message": "User does not exist"}), status=404)
