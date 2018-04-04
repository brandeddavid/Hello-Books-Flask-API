from flask_restful import Resource
from api.models import User, Book
from api.bkendlogic import *
from flask import jsonify, request, make_response, Response, json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity, get_raw_jwt)
from api import app, users, books

jwt = JWTManager(app)

blacklist = set()

b1 = Book('The Lean Start Up', 'Eric Ries', '12345').createbook()
# b2 = Book('A Game of Thrones', 'George R.R. Martin', '67890').createbook()
# b3 = Book('If Tomorrow Comes', 'Sidney Sheldon', '54321').createbook()
user1 = User("dmwangi", 'password', True).createUser()

class GetAllBooks(Resource):

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

            return Response(json.dumps({'Message': 'No Book Information Passed'}), 403)

        if data['title'].strip() == '':
            return Response(json.dumps({'Message': 'Title Not Provided'}), 403)

        if data['author'].strip() == '':
            return Response(json.dumps({'Message': 'Author Not Provided'}), 403)

        if data['isbn'].strip() == '':
            return Response(json.dumps({'Message': 'ISBN Not Provided'}), 403)

        res = Book(title=data['title'].strip(), author=data['author'].strip(),
                   isbn=data['isbn'].strip()).createbook()
        return res


class BookOps(Resource):

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
            return Response(json.dumps({'Message': 'No Book Information Passed'}), status=403)

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

    def post(self):
        """
        [Post method creates a new user]
        Returns:
            [json object] -- [With the approriate response and status code]
        """

        data = request.get_json(self)

        if len(data) == 0:
            return Response(json.dumps({'Message': 'No User Information Passed'}), status=403)

        if data['username'] == '':
            return Response(json.dumps({'Message': 'Username Not Provided'}), status=403)

        if data['password'] == '':
            return Response(json.dumps({'Message': 'Password Not Provided'}), status=403)

        if len(data['password']) < 8:
            return Response(json.dumps({'Message': 'Password too Short'}), status=403)

        hashed_password = generate_password_hash(
            data['password'], method='sha256')
        res = User(username=data['username'],
                   password=hashed_password, admin=False).createUser()
        return res


class GetAllUsers(Resource):

    def get(self):
        """
        [Get method returns a list of all users]

        Returns:
            [json object] -- [With the list of all users]
        """

        return getAllUsers()


class LoginUser(Resource):

    def post(self):
        """
        [Post method passes user info to the login endpoint]

        Returns:
            [json object] -- [With appropriate response and status code]
        """

        data = request.get_json(self)

        if len(data) == 0:
            return Response(json.dumps({'Message': 'User Information Not Passed'}), status=403)

        username = data['username']
        password = data['password']

        if not username:
            return Response(json.dumps({'Message': 'Username Not Provided'}), status=403)

        if not password:
            return Response(json.dumps({'Message': 'Password Not Provided'}), status=403)

        return login(username, password)

class LogoutUser(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return Response(json.dumps({"Message": "Successfully logged out"}), status=200)


class BorrowBook(Resource):
    @jwt_required
    def post(self, book_id):
        """
        [Post method used to pass book id to be borrowed]

        Arguments:
            book_id {[str]} -- [str representation of the book id]

        Returns:
            [json object] -- [With the appropriate response and status code]
        """

        return borrowBook(book_id=book_id)


class UpdatePassword(Resource):

    def post(self, user_id):
        """
        [Post method used to update password]

        Arguments:
            user_id {[str]} -- [str representation of the user id]

        Returns:
            [json object] -- [with the appropriate response and status code]
        """

        data = request.get_json(self)

        users = jsonify(getAllUsers())

        for user in users:

            if user['username'] == data['username']:

                if check_password_hash(user['password'], data['password']):

                    user['password'] = generate_password_hash(
                        data['newpassword'])

                    return updatePassword(id=user_id, username=user['username'], password=user['password'])

        return Response(json.dumps({'Message': 'User Does Not Exist'}), status=404)
