from flask_restful import Resource
from api.models import User, Book
from flask import jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

b1 = Book('The Lean Start Up', 'Eric Ries', '12345').createbook()
b2 = Book('A Game of Thrones', 'George R.R. Martin', '67890').createbook()
b3 = Book('If Tomorrow Comes', 'Sidney Sheldon', '54321').createbook()


class GetAllBooks(Resource):
    """

    """

    def get(self):
        """

        :return:
        """

        return jsonify(Book.get_all_books(), 200)

    def post(self):
        """

        :param book_id:
        :return:
        """

        data = request.get_json(self)

        return jsonify(Book(title=data['title'], author=data['author'], isbn=data['isbn']).createbook(), 201)


class BookOps(Resource):

    def get(self, book_id):
        """
        Function takes in a book id and returns book information for that book
        :param book_id:
        :return: Book Details for book with id book_id
        """

        return jsonify(Book.getbook(id=book_id))

    def put(self, book_id):
        """

        :param book_id:
        :return:
        """

        data = request.get_json(self)

        return jsonify(Book.updatebook(id=book_id, data=data))

    def delete(self, book_id):

        return jsonify(Book.deletebook(id=book_id))

def token_required(f):
    """

    :param f:
    :return:
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        token = None

        if 'x-access-token' in request.headers:

            token = request.headers['x-access-token']

        if not token:

            return jsonify({'Message': 'Token is Missing'})

        try:

            data = jwt.decode(token, 'super-secret-key')
            users = User.getAllUsers()

            for user in users:

                if user['id'] == data['id']:

                    current_user = user
        except:
            return jsonify({'Message': 'Token is Invalid'})

        return f(current_user, *args, **kwargs)

    return decorated


class CreateUser(Resource):

    def post(self):
        """

        :return:
        """
        data = request.get_json(self)
        hashed_password = generate_password_hash(
            data['password'], method='sha256')
        return jsonify(User(id=data['id'], username=data['username'], password=hashed_password, admin=data['admin']).createUser())


class GetAllUsers(Resource):

    @token_required
    def get(self, current_user):
        """

        :param current_user:
        :return:
        """
        return jsonify({"Users": User.getAllUsers()})


class LoginUser(Resource):

    def post(self):
        """

        :return:
        """

        auth = request.authorization

        if not auth or not auth.username or not auth.password:

            return make_response('Could Not Verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

        users = User.getAllUsers()

        for user in users:

            if auth.username in user['username']:

                if check_password_hash(user['password'], auth.password):
                    token = jwt.encode({'id': user['id'], 'exp': datetime.datetime.utcnow(
                    ) + datetime.timedelta(minutes=30)}, 'super-secret-key')

                    return jsonify({'token': token.decode('UTF-8')})

            else:

                return make_response('Could Not Verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

        return make_response('Could Not Verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})


class BorrowBook(Resource):

    @token_required
    def post(self, current_user, book_id):
        """

        :param current_user:
        :param book_id:
        :return:
        """
        return jsonify(User.borrowBook(book_id=book_id))


class UpdatePassword(Resource):

    @token_required
    def post(self, current_user, user_id):
        """

        :param current_user:
        :param user_id:
        :return:
        """
        data = request.get_json(self)

        users = User.getAllUsers()

        for user in users:

            if user['username'] == data['username']:

                if check_password_hash(user['password'], data['password']):

                    user['password'] = generate_password_hash(
                        data['newpassword'])

                    newUser = User.updatePassword(
                        id=user_id, username=user['username'], password=user['password'])
                    return jsonify({'Message': 'Password Reset Successful'})

                else:

                    return jsonify({'Message': 'Passwords Do Not Match'})

            else:

                return jsonify({'Message': 'User Does Not Exist'})
