import unittest
import json
from api.models import Book, User
from api.bkendlogic import getBookId, getUserId
from run import app
from flask import jsonify
from api import users, books

class TestUserAPI(unittest.TestCase):

    def setUp(self):
        """
        Set Up function to run before every test function runs
        """
        app.testing = True
        self.app = app.test_client()
        self.user = User('dmwangi', 'password123')
        users[self.user.id] = self.user

    def tearDown(self):
        """
        Functions does clean up. Runs after every test function runs
        """
        app.testing = False
        self.app = None
        self.user = None

    def test_register_user_success(self):
        """
        Tests 201 status code response when user has been created successfully
        Asserts 201 Created Status Response
        """
        payload = {
            "username": "username",
            "password": "password1234",
            "confirm": "password1234"
        }
        res = self.app.post('/api/v1/auth/register', data=json.dumps(payload))
        self.assertEqual(res.status_code, 201)

    def test_register_user_bad_request(self):
        """
        Tests whether the register user API endpoint can pass a Bad Request(Missing User Information)
        Send a post request to register user API with no user information(Bad Request).
        Asserts 400 Bad Request Status Response
        """
        payload = {}
        res = self.app.post('/api/v1/auth/register', data=json.dumps(payload))
        self.assertEqual(res.status_code, 403)

    def test_register_user_no_username(self):
        """
        Tests 201 status code response when user has been created successfully
        Asserts 201 Created Status Response
        """
        payload = {
            "username": "",
            "password": "password1234",
            "confirm": "password1234"
        }
        res = self.app.post('/api/v1/auth/register', data=json.dumps(payload))
        self.assertEqual(res.status_code, 403)

    def test_register_user_no_password(self):
        """
        Tests 201 status code response when user has been created successfully
        Asserts 201 Created Status Response
        """
        payload = {
            "username": "username",
            "password": "",
            "confirm": "password1234"
        }
        res = self.app.post('/api/v1/auth/register', data=json.dumps(payload))
        self.assertEqual(res.status_code, 403)

    def test_register_user_no_confirm(self):
        """
        Tests 201 status code response when user has been created successfully
        Asserts 201 Created Status Response
        """
        payload = {
            "username": "username",
            "password": "password1234",
            "confirm": ""
        }
        res = self.app.post('/api/v1/auth/register', data=json.dumps(payload))
        self.assertEqual(res.status_code, 403)

    def test_register_user_short_password(self):
        """
        Tests 201 status code response when user has been created successfully
        Asserts 201 Created Status Response
        """
        payload = {
            "username": "username",
            "password": "pas",
            "confirm": "pas"
        }
        res = self.app.post('/api/v1/auth/register', data=json.dumps(payload))
        self.assertEqual(res.status_code, 403)

    def test_get_all_users(self):
        """
        Tests Get All Users API endpoint
        Asserts 200 OK Status Code Response
        """
        res = self.app.get('/api/v1/users')
        self.assertEqual(res.status_code, 200)

    def test_login_successful(self):
        """
        Tests Login API endpoint
        Asserts 200 OK Status Code Response
        """
        payload = {
            "username": "dmwangi",
            "password": "password123",
        }
        res = self.app.post('/api/v1/auth/login', data=json.dumps(payload))
        self.assertEqual(res.status_code, 200)

    def test_login_no_username(self):
        """
        Tests Login API endpoint
        Asserts 200 OK Status Code Response
        """
        payload = {
            "username": "",
            "password": "password123",
        }
        res = self.app.post('/api/v1/auth/login', data=json.dumps(payload))
        self.assertEqual(res.status_code, 403)

    def test_login_no_password(self):
        """
        Tests Login API endpoint
        Asserts 200 OK Status Code Response
        """
        payload = {
            "username": "dmwangi",
            "password": "",
        }
        res = self.app.post('/api/v1/auth/login', data=json.dumps(payload))
        self.assertEqual(res.status_code, 403)

    def test_login_bad_request(self):
        """
        Tests Login API endpoint when an empty object is passed
        Asserts 403 Status Code Response
        """
        payload = {}
        res = self.app.post('/api/v1/auth/login', data=json.dumps(payload))
        self.assertEqual(res.status_code, 403)

    def test_login_user_not_registered(self):
        """
        Tests Login API endpoint
        Asserts 404 OK Status Code Response
        """
        payload = {
            "username": "notauser",
            "password": "password123",
        }
        res = self.app.post('/api/v1/auth/login', data=json.dumps(payload))
        self.assertEqual(res.status_code, 404)

    def test_login_user_wrong_password(self):
        """
        Tests Login API endpoint
        Asserts 404 OK Status Code Response
        """
        payload = {
            "username": "dmwangi",
            "password": "password",
        }
        res = self.app.post('/api/v1/auth/login', data=json.dumps(payload))
        self.assertEqual(res.status_code, 401)

    def test_borrow_book_api_endpoint(self):
        """
        Tests Borrow book API endpoint
        Asserts 200 OK Status Code Response     
        """
        book = Book('Title', 'Author', '34678')
        books[book.id] = book.__dict__
        id = getBookId('34678')
        payload = {
            "username":"dmwangi"
        }
        res = self.app.post('/api/v1/users/books/'+id, data=json.dumps(payload))
        self.assertEqual(res.status_code, 200)

    def test_borrow_book_api_endpoint_non_user(self):
        """
        Tests Borrow book API endpoint
        Asserts 200 OK Status Code Response     
        """
        book = Book('Title', 'Author', '34678')
        books[book.id] = book.__dict__
        id = getBookId('34678')
        payload = {
            "username":"noreg"
        }
        res = self.app.post('/api/v1/users/books/'+id, data=json.dumps(payload))
        self.assertEqual(res.status_code, 200)
        
        

if __name__ == '__main__':
    unittest.main()
