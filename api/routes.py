from flask import Blueprint
from api.api import *
from flask_restful import Api

mod = Blueprint('api', __name__)
api = Api(mod)

api.add_resource(GetAllBooks, '/api/v1/books')
api.add_resource(BookOps, '/api/v1/books/<string:book_id>')
