from flask import Blueprint
from models import *
from flask_restful import Api

mod = Blueprint('api', __name__)
api = Api(mod)

api.add_resource(Book, '/api/v1/books')