# """
# [
#     File maps apiendpoints to resourses serving them
# ]
# """
from flask import Blueprint
from flask_restful import Api
from api.users.views import CreateUser, GetAllUsers
from api.books.views import Books

mod = Blueprint('api', __name__)
api = Api(mod)

api.add_resource(Books, '/api/v1/books')
# api.add_resource(BookOps, '/api/v1/books/<string:book_id>')
# api.add_resource(BorrowBook, '/api/v1/users/books/<string:book_id>')
api.add_resource(GetAllUsers, '/api/v1/users')
api.add_resource(CreateUser, '/api/v1/auth/register')
# api.add_resource(LoginUser, '/api/v1/auth/login')
# api.add_resource(LogoutUser, '/api/v1/auth/logout')
# api.add_resource(UpdatePassword, '/api/v1/auth/reset-password/<string:user_id>')
