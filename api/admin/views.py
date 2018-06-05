from flask_restful import Resource
from flask import json, request, Response
from api.models import Book, User
from flask_jwt_extended import get_current_user, jwt_required


class Books(Resource):
    """[summary]
    
    Arguments:
        Resource {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    @jwt_required
    def post(self):
        try:
            current_user = User.get_user_by_username(get_current_user())
            if current_user.is_admin:
                data = request.get_json(self)
                if len(data) == 0:
                    return Response(json.dumps({"Message": "Book information not passed"}), status=403)
                data['title'] = data['title'].strip().lower().title()
                data['author'] = data['author'].strip().title()
                data['isbn'] = data['isbn'].strip()
                data['publisher'] = data['publisher'].strip().title()
                data['quantity'] = data['quantity']
                if not data['title']:
                    return Response(json.dumps({"Message": "Book title not provided"}), status=403)
                if len(data['title']) > 500:
                    return Response(json.dumps({"Message": "Title exceeds 500 character limit"}), status=403)
                if not data['author']:
                    return Response(json.dumps({"Message": "Book author not provided"}), status=403)
                if len(data['author']) > 100:
                    return Response(json.dumps({"Message": "Author exceeds 500 character limit"}), status=403)
                if not data['isbn']:
                    return Response(json.dumps({"Message": "Book isbn not provided"}), status=403)
                if len(data['isbn']) > 100:
                    return Response(json.dumps({"Message": "ISBN exceeds 500 character limit"}), status=403)
                if not data['publisher']:
                    return Response(json.dumps({"Message": "Book publisher not provided"}), status=403)
                if len(data['publisher']) > 100:
                    return Response(json.dumps({"Message": "Publisher exceeds 500 character limit"}), status=403)
                if not data['quantity']:
                    return Response(json.dumps({"Message": "Book quantity not provided"}), status=403)
                books = Book.all_books()
                isbn = [book for book in books if book.isbn == data['isbn']]
                if isbn:
                    return Response(json.dumps({"Message": "Book already exists"}), status=403)
                Book(data['title'], data['author'], data['isbn'], data['publisher'], data['quantity']).save()
                return Response(json.dumps({"Message": "Book added successfully"}), status=201)
            return Response(json.dumps({"Message": "User not an admin"}), status=401)
        except Exception as e:
            print(e)
            return Response(json.dumps({"Message": "Not logged in"}), status=401)