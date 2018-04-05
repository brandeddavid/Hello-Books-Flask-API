from flask import json, Response
from api import users, books


class User:

    user_id = 1

    def __init__(self, username, password):
        """
        [summary]

        Arguments:
            username {[type]} -- [description]
            password {[type]} -- [description]
            admin {[type]} -- [description]
        """

        self.id = str(User.user_id)
        User.user_id += 1
        self.username = username
        self.password = password
        self.admin = False
        self.borrowedbooks = []


class Book:

    book_id = 1

    def __init__(self, title, author, isbn):
        """
        [summary]

        Arguments:
            title {[type]} -- [description]
            author {[type]} -- [description]
            isbn {str} -- [description]
        """

        self.id = str(Book.book_id)
        Book.book_id += 1
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True
