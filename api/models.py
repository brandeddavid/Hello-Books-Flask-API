from flask import jsonify

books = []
users = []

class User(object):

    def __init__(self):

        self.users = {}

    def createUser(self, fname, sname, username, password):

        user = {}
        user['firstName'] = fname
        user['secondName'] = sname
        user['password'] = password

        try:

            self.users[username] = user
            users.append(self.users)

            return 'User Created Successfully'

        except Exception as e:

            return 'User Already Exists'

    def loginUser(self, username, password):

        for user in users:

            if username in user.keys():

                if user[username]['password'] == password:

                    return 'User Login Successful'

                else:

                    return 'Passwords do not Match'

            else:

                return 'User Not Registered'

    def updatePassword(self, username, oldpassword, newpassword):

        for user in users:

            if username in user.keys():

                if user[username]['password'] == oldpassword:

                    user[username]['password'] = newpassword

                    return 'Password Reset Successful'

                else:

                    return 'Password Mismatch'

            else:

                return 'User Not Registered'

    def deleteUser(self, username):

        for user in users:

            if username in user.keys():

                del user[username]

                return 'User Deleted Successfully'
            else:

                return 'User Not Registered'

    def borrowBook(self, username, password, bookid):
        pass


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

            return "Book Created Successfully"

        else:

            for book in books:

                if self.book['isbn'] in book.values():

                    pass

                else:

                    book = {}
                    book[self.id] = self.book
                    books.append(book)

                    return "Book Created Successfully"



    def get_all_books():

        return books

    def deletebook(id):

        for book in books:

            if id in book.keys():

                books.remove(book)

                return {'Success': 'Book Deleted Successfully'}

            else:

                return {'Error': 'Book Does Not Exist'}

    # def updatebook(self,id, newTitle, newAuthor):
    #
    #     for book in books:
    #
    #         if id in book.keys():
    #
    #             book[id]['title'] = newTitle
    #             book[id]['author'] = newAuthor
    #
    #             return 'Book Update Successful'
    #
    def getbook(id):

        for book in books:

            if id in book.keys():

                return book

            else:

                return {'Error': 'Book Does not Exist'}


def main():


    b = Books()

    b.createbook(2, 'The Lean Start Up', 'Eric Ries')

    b1 = Book('The Lean Start Up', 'Eric Ries', '12345').createbook()
    b2 = Book('A Game of Thrones', 'George R.R. Martin', '67890').createbook()
    b2 = Book('If Tomorrow Comes', 'Sidney Sheldon', '54321').createbook()
    print(books)

if __name__ == '__main__':

    main()

