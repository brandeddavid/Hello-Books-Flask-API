"""File with auth endpoints resources"""

from api import jwt
from api.models import User, Token, Revoked
from api.auth.validate import validate_register, validate_login
from flask_restful import Resource
from flask import json, request, Response
from flask_jwt_extended import create_access_token, get_raw_jwt, get_jwt_identity, jwt_manager, jwt_required


class Register(Resource):
    """Register User Resource"""

    def post(self):
        """Function serving register user api endpoint"""
        data = request.get_json(self)
        if validate_register(data):
            return Response(json.dumps(validate_user(data)), status=403)
        if data['password'] != data['confirm_password']:
            return Response(json.dumps({"Message": "Password provided do not match"}), status=403)
        users = User.all_users()
        email = [user for user in users if user.email == data['email']]
        if email:
            return Response(json.dumps({"Message":"Email provided already exists"}), status=409)
        username = [user for user in users if user.username == data['username']]
        if username:
            return Response(json.dumps({"Message":"Username provided already exists"}), status=409)
        User(data['email'], data['username'], data['first_name'], data['last_name'], data['password']).save()
        return Response(json.dumps({"Message": "User Created Successfully"}), status=201)


class Login(Resource):
    """Login User Resource"""

    def post(self):
        """Function serving login user api endpoint"""
        data = request.get_json(self)
        data['username'] = data['username'].replace(" ", "").lower()
        if validate_login(data):
            return Response(json.dumps(validate_login(data)), status=403)
        users = User.all_users()
        user = [user for user in users if user.username == data['username']]
        if user:
            if User.verify_password(user[0].password_hash, data['password']):
                logged_in = Token.token_by_owner(user[0].username)
                if logged_in:
                    return Response(json.dumps({"Message": "Already logged in", "Token": logged_in.token}), status=403)
                token = create_access_token(identity=user[0].username)
                tk = Token(token, user[0].username).save()
                return Response(json.dumps({"Message": "Successfully logged in", "Token": token}), status=200)
            return Response(json.dumps({"Message": "Passwords do not match"}), status=409)
        return Response(json.dumps({"Message": "User does not exist"}), status=404)
    

class Logout(Resource):
    """Logout User Resource"""

    @jwt_required
    def post(self):
        """Function handling logout user api endpoint"""
        try:
            current_user = get_jwt_identity()
            jti = get_raw_jwt()['jti']
            if not Revoked.is_blacklisted(jti):
                Revoked(jti).save()
                Token.delete(Token.token_by_owner(current_user))
                return Response(json.dumps({"Message": "Logged out successfully"}), status=200)
            return Response(json.dumps({"Message": "User token has been revoked"}), status=403)
        except Exception as e:
            print (e)
            return Response(json.dumps({"Message": "Not logged in"}), status=401)


class ResetPassword(Resource):
    """Reset Password Resource"""

    @jwt_required
    def post(self):
        """Function handling reset password api endpoint"""
        try:
            identity = get_jwt_identity()
            current_user = User.get_user_by_username(identity)
            data = request.get_json(self)
            if validate_reset_password(data):
                return validate_reset_password(data)
            if User.verify_password(current_user.password_hash, data["password"]):
                current_user.update_password(data["password"])
                return Response(json.dumps({"Message": "Password updated successfully"}), status=200)
            return Response(json.dumps({"Message": "Password do not match"}), status=403)
        except Exception as e:
            print(e)
            return Response(json.dumps({"Message": "Not logged in"}), status=401)
