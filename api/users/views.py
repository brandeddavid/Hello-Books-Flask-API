from flask_restful import Resource
from flask import request, json, Response
from api.models import User


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