from flask_restful import Resource
import request
import json

# class Users(object):
#
#     def __init__(self, fname, sname, username, password):
#         self.firstname = fname
#         self.sname = sname
#         self.username = username
#         self.password = password
#
#         self.users = []
#
#     class Createuser(Resource):
#
#         def get(self):
#
#             pass
#
#         def put(self):
#
#             pass
books = []
class Books(object):
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