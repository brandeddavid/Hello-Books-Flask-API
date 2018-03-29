from flask import Blueprint
from api.apis import *
from flask_restful import Api

mod = Blueprint('api', __name__)
api = Api(mod)

api.add_resource(GetAllBooks, '/api/v1/books')
api.add_resource(BookOps, '/api/v1/books/<string:book_id>')
api.add_resource(BorrowBook, '/api/v1/users/books/<string:book_id>')
api.add_resource(GetAllUsers, '/api/v1/users')
api.add_resource(CreateUser, '/api/v1/auth/register')
api.add_resource(LoginUser, '/api/v1/auth/login')
# api.add_resource( '/api/v1/auth/logout')
api.add_resource(UpdatePassword, '/api/v1/auth/reset-password/<string:user_id>')
