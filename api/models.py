from flask import jsonify

books = []
users = []


class User(object):

    def __init__(self, id, username, password, admin):
        """

        :param id:
        :param username:
        :param password:
        :param admin:
        """

        self.user = {}
        self.user['id'] = id
        self.user['username'] = username
        self.user['password'] = password
        self.user['admin'] = admin

    def createUser(self):
        """

        :return:
        """

        if len(users) == 0:
            users.append(self.user)
            return {'Message': 'User Created Successfully'}

        for user in users:

            if user['id'] == self.user['id']:

                return {'Message': 'User id Exists'}

            else:

                if user['username'] == self.user['username']:

                    return {'Message': 'Username Exists'}

                else:

                    users.append(self.user)

                    return {'Message': 'User Created Successfully'}

    def getAllUsers():
        """

        :return:
        """

        return users

    def updatePassword(id, username, password):
        """

        :param username:
        :param password:
        :return:
        """

        for user in users:

            if username in user.values():

                user['password'] = password

                return {'Message': 'User Password Updated Successfully'}

            else:

                return {'Message': 'User Password Update Failed'}


    def borrowBook(book_id):
        """

        :return:
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
        Class Initializes a Book instance with following parameters:
        :param title: Bool Title
        :param author: Book Author
        :param isbn: Book ISBN Number
        """

        self.book = {}
        self.id = str(Book.book_id)
        Book.book_id += 1
        self.book['title'] = title
        self.book['author'] = author
        self.book['isbn'] = isbn

    def createbook(self):
        """
        Functions assigns the book object an id and appends it to the book list
        :return: Success message
        """

        if len(books) == 0:
            book = {}
            book[self.id] = self.book
            books.append(book)

            return {'Success': 'Book Created Successfully'}

        else:

            for book in books:

                if self.id in book.keys():

                    return {'Error': 'Book Already Exists'}

                else:

                    book = {}
                    book[str(self.id)] = self.book
                    books.append(book)

                    return {'Success': 'Book Created Successfully'}

    def apicreatebook(id, data):
        """

        :param data:
        :return:
        """

        for book in books:

            if id in book.keys():

                return {'Error': 'Book Already Exists'}

            else:

                new_book = {str(id): data}
                books.append(new_book)

                return {'Success': 'Book Created Successfully'}

    def get_all_books():
        """

        :return:
        """

        return books

    def deletebook(id):
        """

        :return:
        """

        for book in books:

            if id in book.keys():

                books.remove(book)

                return {'Success': 'Book Deleted Successfully'}

            else:

                return {'Error': 'Book Does Not Exist'}

    def updatebook(id, data):
        """

        :param data:
        :return:
        """

        for book in books:

            if id in book.keys():

                book[id] = data

                return {'Success': 'Book Update Successful'}

            else:

                return {'Error': 'Book Does Not Exist'}

    def getbook(id):
        """

        :return:
        """

        for book in books:

            if id in book.keys():

                return book

            else:

                return {'Error': 'Book Does not Exist'}


def main():

    b1 = Book('The Lean Start Up', 'Eric Ries', '12345').createbook()
    b2 = Book('A Game of Thrones', 'George R.R. Martin', '67890').createbook()
    b2 = Book('If Tomorrow Comes', 'Sidney Sheldon', '54321').createbook()
    print(books)

    user = User(1, 'dmwangi', 'dmwangi123').createUser()
    user = User(2, 'dmwang', 'dmwangi12').createUser()

    print(users)

if __name__ == '__main__':

    main()
