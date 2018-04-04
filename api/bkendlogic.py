from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity, get_raw_jwt)
from api import app, users, books
from flask import jsonify, request, make_response, Response, json

def getAllUsers():
    """
    [summary]

    Returns:
        [type] -- [description]
    """

    if len(users) == 0:

        return Response(json.dumps({'Message': 'No Users'}), status=404)

    return Response(json.dumps({'Users': users}), status=200)


def updatePassword(id, username, password):
    """
    [summary]

    Arguments:
        id {[type]} -- [description]
        username {[type]} -- [description]
        password {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    for user in users:

        if user['username'] == username:

            user['password'] = password

            return Response(json.dumps({'Message': 'User Password Updated Successfully'}), status=200)

        else:

            return Response(json.dumps({'Message': 'User Password Update Failed'}), status=200)

def login(username, password):
    for user in users:

        if user['username'] == username:

            if check_password_hash(user['password'], password):

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

    for book in books:

        if book['id'] == book_id:

            return Response(json.dumps({'Message': 'Successfully Borrowed Book'}), status=200)

    return Response(json.dumps({'Message': 'Book Does Not Exist'}), status=404)


def deleteUser(id):
    for user in users:
        if user['id'] == id:
            users.remove(user)

def getUserId(username):

    for user in users:

        if user['username'] == username:

            return user['id']

# BOOK'S FUNCTIONS


def getAllBooks():
    """
    [summary]

    Returns:
        [type] -- [description]
    """

    if len(books) == 0:
        return Response(json.dumps({'Message': 'No Books'}), status=404)

    return Response(json.dumps({'Books': books}), status=200)


def getBook(id):
    """
    [summary]

    Arguments:
        id {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    for book in books:

        if book['id'] == id:

            return Response(json.dumps(book), status=200)

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

    for book in books:

        if book['id'] == id:

            book['title'] = data['title'].strip()
            book['author'] = data['author'].strip()
            book['isbn'] = data['isbn'].strip()

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
    for book in books:

        if book['id'] == id:

            msg = {'Message': 'Book Deleted Successfully'}
            books.remove(book)

            return Response(json.dumps(msg), status=204)

    return Response(json.dumps({'Message': 'Book Does Not Exist'}), status=404)

def getBookId(isbn):

    for book in books:

        if book['isbn'] == isbn:

            return book['id']

### DANGER ZONE ##
def deleteAllUsers():

    if len(users) == 0:
        pass 
    for user in users:
        users.remove(user)

def deleteAllBooks():

    if len(books) == 0:
        pass 
    for book in books:
        books.remove(book)

    