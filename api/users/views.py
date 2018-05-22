from flask_restful import Resource
from flask import request, json, Response, Markup
from api.models import User

class CreateUser(Resource):
    """
    [summary]
    
    Arguments:
        Resource {[type]} -- [description]
    """
    def post(self):
        """
        [summary]
        
        Returns:
            [type] -- [description]
        """
        data = request.get_json(self)
        data['email'] = data['email'].replace(" ", "").lower()
        data['username'] = data['username'].replace(" ", "").lower()
        data['first_name'] = data['first_name'].replace(" ", "")
        data['last_name'] = data['last_name'].replace(" ", "")
        if len(data) == 0:
            return Response(json.dumps({"Message":"User data information not passed"}), status=403)
        if not data['email']:
            return Response(json.dumps({"Message":"Email not provided"}), status=403)
        if len(data['email']) > 60:
            return Response(json.dumps({"Message":"Email exceeds 60 characters requirement"}), status=403)
        if not data['username']:
            return Response(json.dumps({"Message":"Username not provided"}), status=403)
        if len(data['email']) > 60:
            return Response(json.dumps({"Message":"Username exceeds 60 characters requirement"}), status=403)
        if not data['first_name']:
            return Response(json.dumps({"Message":"First name not provided"}), status=403)
        if len(data['email']) > 60:
            return Response(json.dumps({"Message":"First name exceeds 60 characters requirement"}), status=403)
        if not data['last_name']:
            return Response(json.dumps({"Message":"Last name not provided"}), status=403)
        if len(data['email']) > 60:
            return Response(json.dumps({"Message":"Last name exceeds 60 characters requirement"}), status=403)
        if not data['password']:
            return Response(json.dumps({"Message":"Password not provided"}), status=403)
        users = User.all_users()
        email = [user for user in users if user.email == data['email']]
        if email:
            return Response(json.dumps({"Message":"Email provided already exists"}), status=403)
        username = [user for user in users if user.username == data['username']]
        if username:
            return Response(json.dumps({"Message":"Username provided already exists"}), status=403)
        User(data['email'], data['username'], data['first_name'], data['last_name'], data['password']).save()
        return Response(json.dumps({"Message": "User Created Successfully"}), status=201)

class GetAllUsers(Resource):
    """[summary]
    
    Arguments:
        Resource {[type]} -- [description]
    """
    def get(self):
        allUsers = User.all_users()
        if len(allUsers) == 0:
            return Response(json.dumps({"Message":"No users found"}))
        return Response(json.dumps({"Users":[user.serialize for user in allUsers]}))