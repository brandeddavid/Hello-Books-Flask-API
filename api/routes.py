# """
# [
#     File maps apiendpoints to resourses serving them
# ]
# """
from flask import Blueprint
from flask_restful import Api
from api.users.views import GetAllUsers
from api.books.views import Books, BookOps
from api.auth.views import Register, Login, Logout, ResetPassword

mod = Blueprint('api', __name__)
api = Api(mod)

api.add_resource(Books, '/api/v1/books')
api.add_resource(BookOps, '/api/v1/book/<book_id>')
# api.add_resource(BorrowBook, '/api/v1/users/books/<string:book_id>')
api.add_resource(GetAllUsers, '/api/v1/users')
api.add_resource(Register, '/api/v1/auth/register')
api.add_resource(Login, '/api/v1/auth/login')
api.add_resource(Logout, '/api/v1/auth/logout')
api.add_resource(ResetPassword, '/api/v1/auth/reset-password')
