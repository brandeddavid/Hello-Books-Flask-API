from api import jwt
from api.models import User, Token
from flask_restful import Resource
from flask import json, request, Response
from flask_jwt_extended import create_access_token, get_raw_jwt, get_jwt_identity, jwt_manager, jwt_required


class Register(Resource):
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


class Login(Resource):
    """    
    Arguments:
        Resource {[type]} -- [description]
    """

    def post(self):
        data = request.get_json(self)
        data['username'] = data['username'].replace(" ", "").lower()
        users = User.all_users()
        user = [user for user in users if user.username == data['username']]
        if user:
            if User.verify_password(user[0].password_hash, data['password']):
                token = create_access_token(identity=user[0].username)
                Token(token, user[0].username).save()
                return Response(json.dumps({"Message": "Successfully logged in", "Token": token}), status=200)
            return Response(json.dumps({"Message": "Passwords do not match"}), status=403)
        return Response(json.dumps({"Message": "User does not exist"}), status=404)
