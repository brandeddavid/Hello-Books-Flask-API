from flask import Response, json
import re

def validate_book(data):
    if len(data) == 0:
        return Response(json.dumps({"Message": "Book information not passed"}), status=403)
    data['title'] = data['title'].strip().lower().title()
    data['author'] = data['author'].strip().title()
    data['isbn'] = data['isbn'].strip()
    data['publisher'] = data['publisher'].strip().title()
    if not data['title']:
        return Response(json.dumps({"Message": "Book title not provided"}), status=403)
    if len(data['title']) > 500:
        return Response(json.dumps({"Message": "Title exceeds 500 character limit"}), status=403)
    if not data['author']:
        return Response(json.dumps({"Message": "Book author not provided"}), status=403)
    if len(data['author']) > 100:
        return Response(json.dumps({"Message": "Author exceeds 100 character limit"}), status=403)
    if not data['isbn']:
        return Response(json.dumps({"Message": "Book isbn not provided"}), status=403)
    if len(data['isbn']) > 100:
        return Response(json.dumps({"Message": "ISBN exceeds 100 character limit"}), status=403)
    if not data['publisher']:
        return Response(json.dumps({"Message": "Book publisher not provided"}), status=403)
    if len(data['publisher']) > 100:
        return Response(json.dumps({"Message": "Publisher exceeds 100 character limit"}), status=403)
    if not data['quantity']:
        return Response(json.dumps({"Message": "Book quantity not provided"}), status=403)

def validate_arg(arg):
    try:
        arg= int(arg)
    except Exception as e:
        return Response(json.dumps({"Message": "Invalid argument passed"}), status=400)

def validate_user(data):
    if len(data) == 0:
        return Response(json.dumps({"Message":"User data information not passed"}), status=403)
    data['email'] = data['email'].replace(" ", "").lower()
    data['username'] = data['username'].replace(" ", "").lower()
    data['first_name'] = data['first_name'].replace(" ", "")
    data['last_name'] = data['last_name'].replace(" ", "")
    if not data['email']:
        return Response(json.dumps({"Message":"Email not provided"}), status=403)
    valid_email =re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", data['email'])
    if not valid_email:
        return Response(json.dumps({"Message": "Invalid email address"}), status=400)
    if len(data['email']) > 60:
        return Response(json.dumps({"Message":"Email exceeds 60 characters requirement"}), status=403)
    if not data['username']:
        return Response(json.dumps({"Message":"Username not provided"}), status=403)
    if len(data['username']) > 60:
        return Response(json.dumps({"Message":"Username exceeds 60 characters requirement"}), status=403)
    if not data['first_name']:
        return Response(json.dumps({"Message":"First name not provided"}), status=403)
    if len(data['first_name']) > 60:
        return Response(json.dumps({"Message":"First name exceeds 60 characters requirement"}), status=403)
    if not data['last_name']:
        return Response(json.dumps({"Message":"Last name not provided"}), status=403)
    if len(data['last_name']) > 60:
        return Response(json.dumps({"Message":"Last name exceeds 60 characters requirement"}), status=403)
    if not data['password']:
        return Response(json.dumps({"Message":"Password not provided"}), status=403)
    if len(data['password']) < 8:
        return Response(json.dumps({"Message": "Password less than 8 characters long"}), status=400)
    if not data['confirm_password']:
        return Response(json.dumps({"Message": "Please provide a password confirmaton"}), status=403)
    if data['password'] != data['confirm_password']:
        return Response(json.dumps({"Message": "Passwords do not match"}), status=400)

def validate_reset_password(data):
    if not data:
        return  Response(json.dumps({"Message": "No Data Passed"}), status=403)
    if not data["password"]:
        return Response(json.dumps({"Message": "Current password not provided"}), status=403)
    if not data["newpassword"]:
        return Response(json.dumps({"Message": "New password not provided"}), status=403)
    if not data["confirmpassword"]:
        return Response(json.dumps({"Message": "Password confirmation not provided"}), status=403)
    if data["newpassword"] != data["confirmpassword"]:
        return Response(json.dumps({"Message": "Password confirmation failed"}), status=403)
