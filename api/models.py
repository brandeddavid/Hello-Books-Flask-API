"""
[
    File defines the user, book and the admin classes.
]
"""
from flask import json, Response

from api import users, books


class User(object):
    """
    [
        Class creating a user object
    ]
    """
    user_id = 1

    def __init__(self, username, password):
        """
        [
            Initializes a User Object
        ]
        Arguments:
            username {[str]} -- [User's username]
            password {[str]} -- [User's password]
        """
        self.id = str(User.user_id)
        User.user_id += 1
        self.username = username
        self.password = password
        self.admin = False
        self.borrowedbooks = []


class Admin(User):
    """
    [
        Class inherits from User class and creates an admin
    ]
    Arguments:
        User {[object]} -- [Inherited User object]
    """
    def __init__(self):
        """
        [
            Defines propeerties specific to the admin object
        ]
        """
        self.admin = True
        self.borrowedbooks = None


class Book(object):
    """
    [
        Class creates a book object
    ]
    """
    book_id = 1

    def __init__(self, title, author, isbn):
        """
        [
            Initializes a book object
        ]

        Arguments:
            title {[str]} -- [Book's title]
            author {[str]} -- [Book's author]
            isbn {str} -- [Book's isbn]
        """
        self.id = str(Book.book_id)
        Book.book_id += 1
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True
