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

        except Exception as e:

            return 'User Already Exists'

        finally:

            return 'User Created Successfully'

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
    """"
    """

    def __init__(self):

        self.book = {}

    def createbook(self, id, title, author):
        bookDetails = {}

        bookDetails['title'] = title
        bookDetails['author'] = author

        self.book[id] = bookDetails
        books.append(self.book)

        return 'Book Created Successfully'

    def deletebook(self, id):

        for book in books:

            if id in book.keys():

                del book[id]
                return 'Book Deleted Successfully'

            else:

                return 'Book Not Available'

    def updatebook(self,id, newTitle, newAuthor):

        for book in books:

            if id in book.keys():

                book[id]['title'] = newTitle
                book[id]['author'] = newAuthor

                return 'Book Update Successful'

    def getbook(self, id):

        for book in books:

            if id in book.keys():

                return 'Book Exists'

            else:

                return 'Book Does not Exist'

# b = Books()
#
# b.createbook(2, 'The Lean Start Up', 'Eric Ries')
#
# print(books)