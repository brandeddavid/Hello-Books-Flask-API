import run
from api import app, db
from config import app_config

import unittest
import json


class TestHelloBooks(unittest.TestCase):
    """[summary]
    
    Arguments:
        unittest {[type]} -- [description]
    """

    def setUp(self):
        self.app = app
        app.config.from_object(app_config['testing'])
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Registration Test Data
        self.user_data = {
            "email":"geof@yahoo.com",
            "username":"geof",
            "first_name":"Geof",
            "last_name":"Humphrey",
            "password":"password1234"
        }
        self.user_data2 = {
            "email":"hump@yahoo.com",
            "username":"geof",
            "first_name":"Geof",
            "last_name":"Humphrey",
            "password":"password1234"
        }
        self.empty_user_data = {

        }
        self.user_data_no_email = {
            "email":"",
            "username":"geof",
            "first_name":"Geof",
            "last_name":"Humphrey",
            "password":"password1234"
        }
        self.user_data_wrong_email = {
            "email":"hgtfd",
            "username":"geof",
            "first_name":"Geof",
            "last_name":"Humphrey",
            "password":"password1234"
        }
        self.user_data_long_email = {
            "email":"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn@gmail.com",
            "username":"geof",
            "first_name":"Geof",
            "last_name":"Humphrey",
            "password":"password1234"
        }
        self.user_data_no_username = {
            "email":"geof@yahoo.com",
            "username":"",
            "first_name":"Geof",
            "last_name":"Humphrey",
            "password":"password1234"
        }
        self.user_data_long_username = {
            "email":"geof@yahoo.com",
            "username":"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn",
            "first_name":"Geof",
            "last_name":"Humphrey",
            "password":"password1234"
        }
        self.user_data_no_first_name = {
            "email":"geof@yahoo.com",
            "username":"geof",
            "first_name":"",
            "last_name":"Humphrey",
            "password":"password1234"
        }
        self.user_data_long_first_name = {
            "email":"geof@yahoo.com",
            "username":"geof",
            "first_name":"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn",
            "last_name":"Humphrey",
            "password":"password1234"
        }
        self.user_data_no_last_name = {
            "email":"geof@yahoo.com",
            "username":"geof",
            "first_name":"Geof",
            "last_name":"",
            "password":"password1234"
        }
        self.user_data_long_last_name = {
            "email":"geof@yahoo.com",
            "username":"geof",
            "first_name":"Geof",
            "last_name":"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn",
            "password":"password1234"
        }
        self.user_data_no_password = {
            "email":"geof@yahoo.com",
            "username":"geof",
            "first_name":"Geof",
            "last_name":"Humphrey",
            "password":""
        }
        self.user_data_short_password = {
            "email":"geof@yahoo.com",
            "username":"geof",
            "first_name":"Geof",
            "last_name":"Humphrey",
            "password":"pass"
        }
        
        #Login Test Data
        self.login_data = {
            "username": "geof",
            "password": "password1234"
        }
        self.login_data_user_not_exist = {
            "username": "harry",
            "password": "password1234"
        }
        self.login_data_password_mismatch = {
            "username": "geof",
            "password": "password123"
        }

    def tearDown(self):
        db.session.close()
        db.drop_all()
        self.app_context.pop()

    def register_user(self, data):
        return self.client.post('/api/v1/auth/register', data=json.dumps(data), content_type='application/json')

    def login_user(self, data):
        return self.client.post('/api/v1/auth/login', data=json.dumps(data), content_type='application/json')
