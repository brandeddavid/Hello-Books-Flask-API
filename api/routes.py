"""
[
    File maps api endpoints to resourses serving them
]
"""
from flask import Blueprint
from flask_restful import Api
from api.users.views import GetAllUsers, BorrowOps, BorrowHistory, PromoteUser
from api.admin.views import AddBook, BookOps
from api.books.views import GetBooks, GetBook
from api.auth.views import Register, Login, Logout, ResetPassword

mod = Blueprint('api', __name__)
api = Api(mod)

api.add_resource(AddBook, '/api/v1/books')
api.add_resource(GetBooks, '/api/v1/books')
api.add_resource(GetBook, '/api/v1/book/<book_id>')
api.add_resource(BookOps, '/api/v1/book/<book_id>')
api.add_resource(GetAllUsers, '/api/v1/users')
api.add_resource(BorrowOps, '/api/users/books/<book_id>')
api.add_resource(BorrowHistory, '/api/users/books')
api.add_resource(Register, '/api/v1/auth/register')
api.add_resource(Login, '/api/v1/auth/login')
api.add_resource(Logout, '/api/v1/auth/logout')
api.add_resource(ResetPassword, '/api/v1/auth/reset-password')
api.add_resource(PromoteUser, '/api/v1/user/promote')
