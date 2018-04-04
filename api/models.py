from flask import json, Response
from api import users, books


class User(object):

    user_id = 1

    def __init__(self, username, password, admin):
        """
        [summary]

        Arguments:
            username {[type]} -- [description]
            password {[type]} -- [description]
            admin {[type]} -- [description]
        """

        self.user = {}
        self.user['id'] = str(User.user_id)
        User.user_id += 1
        self.user['username'] = username
        self.user['password'] = password
        self.user['admin'] = admin

    def createUser(self):
        """
        [Summary]

        Returns:
            [type] -- [description]
        """

        if len(users) == 0:
            users.append(self.user)
            return Response(json.dumps({'Message': 'User Created Successfully'}), status=201)

        for user in users:

            if user['username'] == self.user['username']:

                return Response(json.dumps({'Message': 'Username Exists'}), status=409)

        users.append(self.user)

        return Response(json.dumps({'Message': 'User Created Successfully'}), status=201)


class Book(object):

    book_id = 1

    def __init__(self, title, author, isbn):
        """
        [summary]

        Arguments:
            title {[type]} -- [description]
            author {[type]} -- [description]
            isbn {bool} -- [description]
        """

        self.book = {}
        self.id = str(Book.book_id)
        Book.book_id += 1
        self.book['id'] = self.id
        self.book['title'] = title
        self.book['author'] = author
        self.book['isbn'] = isbn

    def createbook(self):
        """
        [summary]

        Returns:
            [type] -- [description]
        """

        if len(books) == 0:
            books.append(self.book)
            return Response(json.dumps({'Message': 'User Created Successfully'}), status=201)

        else:

            for book in books:

                if book['isbn'] == self.book['isbn']:

                    return Response(json.dumps({'Message': 'Book Already Exists'}), status=409)

            books.append(self.book)

            return Response(json.dumps({'Message': 'Book Created Successfully'}), status=201)
