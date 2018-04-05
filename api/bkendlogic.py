from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity, get_raw_jwt)
from api import app, users, books
from flask import jsonify, request, make_response, Response, json
from api.models import Book, User

def createBook(data):
        """
        [summary]

        Returns:
            [type] -- [description]
        """

        if len(books) == 0:
            book = Book(data['title'], data['author'], data['isbn'])
            books[book.id] = book.__dict__
            return Response(json.dumps({'Message': 'User Created Successfully'}), status=201)

        else:

            for key in books:

                if books[key]['isbn'] == data['isbn']:

                    return Response(json.dumps({'Message': 'Book Already Exists'}), status=409)

            book = Book(data['title'], data['author'], data['isbn'])
            books[book.id] = book.__dict__

            return Response(json.dumps({'Message': 'Book Created Successfully'}), status=201)
        
def getAllBooks():
    """
    [summary]

    Returns:
        [type] -- [description]
    """

    if len(books) == 0:
        return Response(json.dumps({'Message': 'No Books'}), status=404)

    return Response(json.dumps(books), status=200)

def getBook(id):
    """
    [summary]

    Arguments:
        id {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    for key in books:

        if key == id:

            return Response(json.dumps(books[key]), status=200)

    return Response(json.dumps({'Message': 'Book Does Not Exist'}), status=404)

def updateBook(id, data):
    """
    [summary]

    Arguments:
        id {[type]} -- [description]
        data {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    for key in books:

        if books[key]['id'] == id:

            books[key]['title'] = data['title'].strip()
            books[key]['author'] = data['author'].strip()
            books[key]['isbn'] = data['isbn'].strip()

            return Response(json.dumps({'Message': 'Book Updated Successfully'}), status=200)

    return Response(json.dumps({'Message': 'Book Does Not Exist'}), status=404)

def deleteBook(id):
    """
    [summary]

    Arguments:
        id {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    for key in books:

        if key == id:

            msg = {'Message': 'Book Deleted Successfully'}
            del(books[key])

            return Response(json.dumps(msg), status=204)

    return Response(json.dumps({'Message': 'Book Does Not Exist'}), status=404)


def createUser(data):
        """
        [Summary]

        Returns:
            [type] -- [description]
        """
        hashed_password = generate_password_hash(data['password'], method='sha256')

        if len(users) == 0:
            user = User(data['username'], hashed_password)
            users[user.id] = user.__dict__
            return Response(json.dumps({'Message': 'User Created Successfully'}), status=201)

        for key in users:

            if users[key]['username'] == data['username']:

                return Response(json.dumps({'Message': 'Username Exists'}), status=409)

        user = User(data['username'], hashed_password)
        users[user.id] = user.__dict__

        return Response(json.dumps({'Message': 'User Created Successfully'}), status=201)

def getAllUsers():
    """
    [summary]

    Returns:
        [type] -- [description]
    """

    if len(users) == 0:

        return Response(json.dumps({'Message': 'No Users'}), status=404)

    return Response(json.dumps(users), status=200)

def login(username, password):
    for key in users:

        if users[key]['username'] == username:

            if check_password_hash(users[key]['password'], password):

                access_token = create_access_token(identity=username)
                return Response(json.dumps({'access_token': access_token}), status=200)

            return Response(json.dumps({'Message': 'Invalid Password'}), status=401)

    return Response(json.dumps({'Message': 'User Does Not Exist'}), status=404)

def borrowBook(book_id):
    """
    [summary]

    Arguments:
        book_id {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    for key in books:

        if books[key]['id'] == book_id:
            
            books[key]['available'] = False
            return Response(json.dumps({'Message': 'Successfully Borrowed Book'}), status=200)

    return Response(json.dumps({'Message': 'Book Does Not Exist'}), status=404)


def updatePassword(id, data):
    """
    [summary]

    Arguments:
        id {[type]} -- [description]
        username {[type]} -- [description]
        password {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    for key in users:

        if users[key]['username'] == data['username']:

            if check_password_hash(users[key]['password'], data['password']):

                users[key]['password'] = generate_password_hash(
                    data['newpassword'])
                return Response(json.dumps({'Message': 'User Password Updated Successfully'}), status=200)

        return Response(json.dumps({'Message': 'User Does Not Exist'}), status=404)

    return Response(json.dumps({'Message': 'User Password Update Failed'}), status=200)

def deleteUser(id):
    for key in users:
        if users[key]['id'] == id:
            del(books[key])

def getUserId(username):

    for key in users:

        if users[key]['username'] == username:

            return users[key]['id']

def getBookId(isbn):

    for key in books:

        if books[key]['isbn'] == isbn:

            return books[key]['id']

### DANGER ZONE ##


def deleteAllUsers():

    if len(users) == 0:
        pass
    for key in users:
        del(books[key])


def deleteAllBooks():

    if len(books) == 0:
        pass
    for key in books:
        del(books[key])
