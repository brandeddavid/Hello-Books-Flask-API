from flask_restful import Resource
class Book(Resource):
    def get(self):
        book = {'Hello': 'World'}

        return book