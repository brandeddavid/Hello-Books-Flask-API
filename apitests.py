import unittest
import json
from api.models import *
from run import app
from flask import jsonify


class TestUserAPI(unittest.TestCase):

    def setUp(self):
        """

        :return:
        """
        app.testing = True
        self.app = app.test_client()
        self.user = User('dmwangi', 'password123', 'True').createUser()

    def tearDown(self):
        """

        :return:
        """
        app.testing = False
        self.app = None

    def test_register_user_bad_request(self):
        """
        Tests whether the register user API endpoint can pass a Bad Request(Missing User Information)
        Send a post request to register user API with no user information(Bad Request).
        :return: 400 Bad Request Status Response
        """
        res = self.app.post('/api/v1/auth/register', data={})
        self.assertEqual(res.status_code, 400)

    def test_register_user_success(self):
        """
        Tests 201 status code response when user has been created successfully
        :return: 201 Created Status Response
        """
        payload = {
            "username": "username",
            "password": "password",
            "admin": "True"
        }
        res = self.app.post('/api/v1/auth/register', data=json.dumps(payload))
        self.assertEqual(res.status_code, 201)

    def test_get_all_user_api_exits(self):
        """

        :return:
        """
        res = self.app.get('/api/v1/users')
        self.assertEqual(res.status_code, 200)

    def test_borrow_book_api_endpoint(self):
        """

        :return:
        """
        res = self.app.post('/api/v1/users/books/<string:book_id>')
        self.assertEqual(res.status_code, 200)

    def test_update_password_exists(self):
        """

        :return:
        """
        res = self.app.post('/api/v1/auth/reset-password/<string:user_id>')
        self.assertEqual(res.status_code, 200)
        

if __name__ == "__main__":
    unittest.main()
