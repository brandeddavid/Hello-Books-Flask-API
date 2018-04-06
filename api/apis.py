"""
This file defines resources and methods that serve \
endpoints within the application.
User input validation is also handled in this file.
"""
from flask_restful import Resource
from flask import request, Response, json
from flask_jwt_extended import (get_jwt_identity, get_raw_jwt)
from flask_jwt_extended import (JWTManager, jwt_required)

from api.bkendlogic import getBook, createBook, updateBook, deleteBook
from api.bkendlogic import getAllUsers, login, updatePassword, borrowBook
from api.bkendlogic import createUser, getAllBooks
from api import app, blacklist
from api.models import Admin

jwt = JWTManager(app)


# b1 = Book('The Lean Start Up', 'Eric Ries', '12345')
# books[b1.id] = b1.__dict__
# b2 = Book('A Game of Thrones', 'George R.R. Martin', '67890')
# books[b2.id] = b2.__dict__
# b3 = Book('If Tomorrow Comes', 'Sidney Sheldon', '54321')
# books[b3.id] = b3.__dict__
# user1 = User("dmwangi", 'password')
# users[user1.id] = user1.__dict__


class Books(Resource):
    """
    Resource with methods serving the Books api endpoints
    """

    def get(self):
        """
        Get method returns json object with list of all books

        Returns:
            [json object] -- [With a list of all books]
        """

        return getAllBooks()

    def post(self):
        """
        Post Method is user to add/create new book

        Returns:
            [json object] -- [Has appropriate message and correct status code]
        """

        data = request.get_json(self)
        if len(data) == 0:
            return Response(json.dumps({'Message': 'No Book Information\
             Passed'}), 403)
        if data['title'].strip() == '':
            return Response(json.dumps({'Message': 'Title Not Provided'}), 403)
        if data['author'].strip() == '':
            return Response(json.dumps({'Message': 'Author Not \
            Provided'}), 403)
        if data['isbn'].strip() == '':
            return Response(json.dumps({'Message': 'ISBN Not Provided'}), 403)
        return createBook(data)


class BookOps(Resource):
    """
    [Class handling book ops methods]
    """
    def get(self, book_id):
        """
        Get Method returns single book

        Arguments:
            book_id {str} -- [str representattion of the book id]

        Returns:
            [json object] -- [Has appropriate response and status code]
        """

        return getBook(id=book_id)

    def put(self, book_id):
        """
        Put Method updates book informatio

        Arguments:
            book_id {[str]} -- [str representation of the book id]

        Returns:
            [json object] -- [With the appropriate response and status code]
        """

        data = request.get_json(self)
        if len(data) == 0:
            return Response(json.dumps({'Message': 'No Book Information \
            Passed'}), status=403)
        if data['title'].strip() == '':
            return Response(json.dumps({'Message': 'Title Not Provided'}), 403)
        if data['author'].strip() == '':
            return Response(json.dumps({'Message': 'Author Not \
            Provided'}), 403)
        if data['isbn'].strip() == '':
            return Response(json.dumps({'Message': 'ISBN Not Provided'}), 403)
        return updateBook(id=book_id, data=data)

    def delete(self, book_id):
        """
        [Delete method deletes a book]

        Arguments:
            book_id {[str]} -- [str representation of the book id]

        Returns:
            [json object] -- [With the appropriate response and status code]
        """
        return deleteBook(id=book_id)


class CreateUser(Resource):
    """
    [Class handling method for user creation]
    """
    def post(self):
        """
        [Post method creates a new user]
        Returns:
            [json object] -- [With the approriate response and status code]
        """

        data = request.get_json(self)

        if len(data) == 0:
            return Response(json.dumps({'Message': 'No User Information \
            Passed'}), status=403)
        if data['username'].strip() == '':
            return Response(json.dumps({'Message': 'Username Not \
            Provided'}), status=403)
        if data['password'].strip() == '':
            return Response(json.dumps({'Message': 'Password Not \
            Provided'}), status=403)
        if data['confirm'].strip() == '':
            return Response(json.dumps({'Message': 'Required to Confirm \
            Password'}), status=403)
        if len(data['password']) < 8:
            return Response(json.dumps({'Message': 'Password too Short. \
            Should be a min of 8 characters'}), status=403)
        if data['password'] != data['confirm']:
            return Response(json.dumps({"Message": "Passwords Do Not \
            Match"}), status=403)
        return createUser(data)


class GetAllUsers(Resource):
    """
    [Class handling method to get all users]
    """
    def get(self):
        """
        [Get method returns a list of all users]

        Returns:
            [json object] -- [With the list of all users]
        """

        return getAllUsers()


class LoginUser(Resource):
    """
    [Class to handle login endpoint method]
    """
    def post(self):
        """
        [Post method passes user info to the login endpoint]

        Returns:
            [json object] -- [With appropriate response and status code]
        """
        data = request.get_json(self)
        if len(data) == 0:
            return Response(json.dumps({'Message': 'User Login Not \
            Passed'}), status=403)
        username = data['username'].strip()
        password = data['password'].strip()
        if not username:
            return Response(json.dumps({'Message': 'Username Not \
            Provided'}), status=403)
        if not password:
            return Response(json.dumps({'Message': 'Password Not \
            Provided'}), status=403)
        return login(username, password)


class LogoutUser(Resource):
    """
    [Class handles logout method]
    Returns:
        [json object] -- [Returns appropriate response and status code]
    """
    @jwt_required
    def post(self):
        """
        [Function revokes logged in users thus logging them out]
        """

        jti = get_raw_jwt()['jti']
        print(jti)
        blacklist.add(jti)
        return Response(json.dumps({"Message": "Successfully \
        logged out"}), status=200)


class BorrowBook(Resource):
    """
    [
        Class with method that serves the borrow book api endpoint
    ]
    """
    def post(self, book_id):
        """
        [
            Post method used to pass book id of the book to be borrowed
            alongside the username of the borrower.
        ]
        Arguments:
            book_id {[str]} -- [str representation of the book id]

        Returns:
            [json object] -- [With the appropriate response and status code]
        """
        data = request.get_json(self)
        return borrowBook(book_id=book_id, data=data)


class UpdatePassword(Resource):
    """
    [class to update user password]
    """
    def post(self, user_id):
        """
        [Post method used to update password]
        Arguments:
            user_id {[str]} -- [str representation of the user id]
        Returns:
            [json object] -- [with the appropriate response and status code]
        """
        data = request.get_json(self)
        if len(data) == 0:
            return Response(json.dumps({'Message': 'User Login Not \
            Passed'}), status=403)
        username = data['username'].strip()
        password = data['password'].strip()
        if not username:
            return Response(json.dumps({'Message': 'Username Not \
            Provided'}), status=403)
        if not password:
            return Response(json.dumps({'Message': 'Password Not \
            Provided'}), status=403)
        return updatePassword(user_id, data)
