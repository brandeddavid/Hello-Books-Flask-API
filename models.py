from flask_restful import Resource
import request
import

books = []
users = []

class User(object):

    def __init__(self):

        self.users = {}

    def createuser(self, fname, sname, username, password):
        pass
        # self.firstname = fname
        # self.sname = sname
        # self.username = username
        # self.password = password

    def loginuser(self, username, password):
        pass

    def updatepassword(self, username, oldpassword, newpassword):
        pass

    def deleteuser(self, username, password):
        pass

    def borrowbook(self, username, password, bookid):
        pass

class Book(object):
    """"
    """

    def __init__(self):

        self.book = {}

    def createbook(self, id, title, author):
        pass

        # bookDetails = {}
        #
        # bookDetails['Title'] = title
        # bookDetails['Auhor'] = author
        #
        # self.book[id] = bookDetails
        # books.append(self.book)
        #
        # return books

    def deletebook(self, id):
        pass

    def updatebook(self,id):
        pass

    def getbook(self, id):
        pass

b = Books()

b.createbook(2, 'The Lean Start Up', 'Eric Ries')

print(books)