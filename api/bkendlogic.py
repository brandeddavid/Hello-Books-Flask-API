"""
[
    File handling most backend logic. Stroring and retrieving data from
    the in memory data structure.
]

"""

from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity, get_raw_jwt)
from flask import jsonify, request, make_response, Response, json

from api import app, users, books
from api.models import Book, User


def createBook(data):
    """
    [
        Function creates a book object and persists it to \
        an in memory data structure
    ]

    Returns:
        [json object] -- [With appropriate message and status code]
    """

    if len(books) == 0:
        book = Book(data['title'], data['author'], data['isbn'])
        books[book.id] = book.__dict__
        return Response(json.dumps({'Message': 'Book Created \
        Successfully'}), status=201)
    else:
        for key in books:
            if books[key]['isbn'] == data['isbn']:
                return Response(json.dumps({'Message': 'Book Already \
                Exists'}), status=409)
        book = Book(data['title'], data['author'], data['isbn'])
        books[book.id] = book.__dict__
        return Response(json.dumps({'Message': 'Book Created \
        Successfully'}), status=201)


def getAllBooks():
    """
    [Book returns data structure containing all book objects]

    Returns:
        [json object] -- [With appropriate message and status code]
    """

    if len(books) == 0:
        return Response(json.dumps({'Message': 'No Books'}), status=404)
    return Response(json.dumps(books), status=200)


def getBook(id):
    """
    [Function returns single book]

    Arguments:
        id {[type]} -- [str representation of the book id]

    Returns:
        [json object] -- [With appropriate message and status code]
    """

    for key in books:
        if key == id:
            return Response(json.dumps(books[key]), status=200)
    return Response(json.dumps({'Message': 'Book Does Not Exist'}), status=404)


def updateBook(id, data):
    """
    [Function update a book]

    Arguments:
        id {[str]} -- [id of book to be updated]
        data {[json]} -- [key-value pairs of the book info to be updated]

    Returns:
        [json object] -- [With appropriate message and status code]
    """

    for key in books:
        if books[key]['id'] == id:
            books[key]['title'] = data['title'].strip()
            books[key]['author'] = data['author'].strip()
            books[key]['isbn'] = data['isbn'].strip()
            return Response(json.dumps({'Message': 'Book Updated \
            Successfully'}), status=200)
    return Response(json.dumps({'Message': 'Book Does Not Exist'}), status=404)


def deleteBook(id):
    """
    [Function deletes book]

    Arguments:
        id {[str]} -- [id of book to be deleted]

    Returns:
        [json object] -- [With appropriate message and status code]
    """
    for key in books:
        if key == id:
            msg = {'Message': 'Book Deleted Successfully'}
            del(books[key])
            return Response(json.dumps(msg), status=204)
    return Response(json.dumps({'Message': 'Book Does Not Exist'}), status=404)


def createUser(data):
    """
    [Function creates user]

    Returns:
        [json object] -- [With appropriate message and status code]
    """
    hashed_password = generate_password_hash(data['password'], method='sha256')
    if len(users) == 0:
        user = User(data['username'].strip().lower(), hashed_password)
        users[user.id] = user.__dict__
        return Response(json.dumps({'Message': 'User Created\
 Successfully'}), status=201)
    for key in users:
        if users[key]['username'] == data['username']:
            return Response(json.dumps({'Message': 'Username Exists'}),
                status=409)
    user = User(data['username'], hashed_password)
    users[user.id] = user.__dict__
    return Response(json.dumps({'Message': 'User Created\
    Successfully'}), status=201)


def getAllUsers():
    """
    [Function gets all users]

    Returns:
        [json object] -- [With appropriate message and status code
        or a data srtructure with all users
    ]
    """
    if len(users) == 0:
        return Response(json.dumps({'Message': 'No Users'}), status=404)
    return Response(json.dumps(users), status=200)


def login(username, password):
    """
    [Function logs in users]
    Arguments:
        username {[str]} -- [user's username]
        password {[str]} -- [user's password]
    Returns:
        [
            json object] -- [With appropriate message and status code
            or an access token for successfully authenticated users
        ]
    """
    for key in users:
        if users[key]['username'] == username:
            if check_password_hash(users[key]['password'], password):
                access_token = create_access_token(identity=username)
                return Response(json.dumps({'access_token': access_token}),
                 status=200)
            return Response(json.dumps({'Message': 'Invalid Password'}),
            status=401)
    return Response(json.dumps({'Message': 'User Does Not Exist'}), status=404)


def borrowBook(book_id, data):
    """
    [Function has borrow book logic]

    Arguments:
        book_id {[str]} -- [id of the book to be borrowerd]
        data{[json]} -- [json objest with the username of the borrower]
    Returns:
        [type] -- [description]
    """
    id = getUserId(data['username'])
    if not id:
        return Response(json.dumps({'Message': 'User Does Not Exist'}), status=404)
    for key in users:
        if key == id:
            user = users[key]
    if len(books) == 0:
        return Response(json.dumps({'Message': 'No Books Available'}), status=404)
    else:
        if book_id not in books.keys():
            return Response(json.dumps({'Message': 'Book Not Available'}), status=404)
        for key in books:
            if books[key]['id'] == book_id:
                if books[key]['available'] == True:
                    book = books[key]
            else:
                    return Response(json.dumps({"Message": "Book Not Available"}),
             status=403)    
    if len(user['borrowedbooks']) == 0:
        user['borrowedbooks'].append(book_id)
        book['available'] = False
        return Response(json.dumps({'Message': 'Successfully Borrowed Book'}),
         status=200)
    for bookid in user['borrowedbooks']:
        if bookid == book_id:
            return Response(json.dumps({"Message": "Book Already Borrowed"}),
             status=403)
    user['borrowedbooks'].append(book_id)
    book['available'] = False
    return Response(json.dumps({'Message': 'Successfully Borrowed Book'}),
     status=200)


def updatePassword(id, data):
    """
    [Function updates user's password]

    Arguments:
        id {[str]} -- [id of the user]
        data{[json]} -- [With user's username and new password]

    Returns:
        [json object] -- [With appropriate message and status code]
    """
    for key in users:
        if users[key]['username'] == data['username']:
            if check_password_hash(users[key]['password'], data['password']):
                users[key]['password'] = generate_password_hash(
                    data['newpassword'])
                return Response(json.dumps({'Message': 'User Password \
                Updated Successfully'}), status=200)
        return Response(json.dumps({'Message': 'User Does \
        Not Exist'}), status=404)
    return Response(json.dumps({'Message': 'User Password \
    Update Failed'}), status=200)


def deleteUser(id):
    """
    [Function Deletes User]
    Arguments:
        id {[str]} -- [id of the user to be deleted]
    """

    for key in users:
        if users[key]['id'] == id:
            del(books[key])


def getUserId(username):
    """
    [Fuction gets user's username from their id]
    Arguments:
        username {[str]} -- [user's username]
    Returns:
        [str] -- [id of the user]
    """
    if len(users) == 0:
        user = None
        return user
    for key in users:
        if users[key]['username'] == username:
            return users[key]['id']


def getBookId(isbn):
    """
    [Fuction gets books's id from its isbn]
    Arguments:
        isbn {[str]} -- [Book's isbn]
    Returns:
        [str] -- [id of the book]
    """
    if len(books) == 0:
        book = None
        return book
    for key in books:
        if books[key]['isbn'] == isbn:
            return books[key]['id']

# DANGER ZONE


def deleteAllUsers():
    """
    [Function deletes all users]
    """
    if len(users) == 0:
        pass
    for key in users:
        del(books[key])


def deleteAllBooks():
    """
    [Function deletes all books]
    """
    for key in books:
        del(books[key])
