from flask_restful import Resource
from api.models import *
from flask import jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, datetime

b1 = Book('The Lean Start Up', 'Eric Ries', '12345').createbook()
b2 = Book('A Game of Thrones', 'George R.R. Martin', '67890').createbook()
b2 = Book('If Tomorrow Comes', 'Sidney Sheldon', '54321').createbook()


class GetAllBooks(Resource):
    """"
    """
    def post(self):

        pass

    def get(self):

        return jsonify(Book.get_all_books())


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


class CreateUser(Resource):

    def post(self):
        data = request.get_json(self)
        hashed_password = generate_password_hash(data['password'], method='sha256')
        return jsonify(User(id=data['id'], username=data['username'], password=hashed_password).createUser())

class GetAllUsers(Resource):

    def get(self):

        return jsonify({"Users": User.getAllUsers()})

class LoginUser(Resource):

    def post(self):

        auth = request.authorization

        if not auth or not auth.username or not auth.password:

            return make_response('Could Not Verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

        users = User.getAllUsers()

        for user in users:

            if auth.username in user['username']:

                if check_password_hash(user['password'], auth.password):
                    token = jwt.encode({'id': user['id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=2)}, 'super-secret-key')

                    return jsonify({'token': token.decode('UTF-8')})

            else:

                return make_response('Could Not Verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

        return make_response('Could Not Verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})


class BorrowBook(Resource):

    def post(self, book_id):

        return jsonify(User.borrowBook(book_id=book_id))


class UpdatePassword(Resource):
    def post(self, user_id):
        data = request.get_json(self)

        users = User.getAllUsers()

        for user in users:

            if user['username'] == data['username']:

                if check_password_hash(user['password'], data['password']):

                    user['password'] = generate_password_hash(data['newpassword'])

                    newUser = User(id=user_id, username=user['username'], password=user['password']).createUser()
                    return jsonify({'Message': 'Password Reset Successful'})

                else:

                    return jsonify({'Message': 'Passwords Do Not Match'})

            else:

                return jsonify({'Message': 'User Does Not Exist'})
