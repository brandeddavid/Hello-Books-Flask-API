from flask import jsonify

books = []
users = []


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
            return {'Message': 'User Created Successfully'}

        for user in users:

            if user['username'] == self.user['username']:

                return {'Message': 'Username Exists'}

        users.append(self.user)

        return {'Message': 'User Created Successfully'}

    def getAllUsers():
        """
        [summary]

        Returns:
            [type] -- [description]
        """

        return users

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

            if username in user.values():

                user['password'] = password

                return {'Message': 'User Password Updated Successfully'}

            else:

                return {'Message': 'User Password Update Failed'}

    def borrowBook(book_id):
        """
        [summary]

        Arguments:
            book_id {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        for book in books:

            if book_id in book.keys():

                return {'Message': 'Successfully Borrowed Book'}

            else:

                return {'Message': 'Book Does Not Exist'}


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
            return {'Success': 'Book Created Successfully'}

        else:

            for book in books:

                if book['isbn'] == self.book['isbn']:

                    return {'Message': 'Book Already Exists'}

            books.append(self.book)

            return {'Success': 'Book Created Successfully'}

    def get_all_books():
        """
        [summary]

        Returns:
            [type] -- [description]
        """

        return books

    def deletebook(id):
        """
        [summary]

        Arguments:
            id {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        for book in books:

            if book['id'] == id:

                books.remove(book)

                return {'Message': 'Book Deleted Successfully'}

        return {'Message': 'Book Does Not Exist'}

    def updatebook(id, data):
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

                book['title'] = data['title']
                book['author'] = data['author']
                book['isbn'] = data['isbn']

                return {'Message': 'Book Update Successful'}

        return {'Message': 'Book Does Not Exist'}

    def getbook(id):
        """
        [summary]

        Arguments:
            id {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        for book in books:

            if book['id'] == id:

                return book

        return {'Message': 'Book Does not Exist'}
