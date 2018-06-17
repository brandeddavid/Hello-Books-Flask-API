from api import app, db
from config import app_config
import run

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

        self.user_data = {
            "email":"geof@yahoo.com",
            "username":"geof",
            "first_name":"Geof",
            "last_name":"Humphrey",
            "password":"password1234"
        }
        self.empty_user_data = {

        }

    def tearDown(self):
        db.session.close()
        db.drop_all()
        self.app_context.pop()

    def register_user(self, data):
        return self.client.post('/api/v1/auth/register', data=json.dumps(data), content_type='application/json')
