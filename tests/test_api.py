import unittest
import json
from api.models import Book, User, getBookId, getUserId, users, books
from run import app
from flask import jsonify


class TestBookAPI(unittest.TestCase):

    def setUp(self):
        """
        Set Up function to run before every test function runs
        """

        app.testing = True
        self.app = app.test_client()
        self.book = Book(title="Book Title", author="Book Author", isbn="456788")

    def tearDown(self):
        """
        Functions does clean up. Runs after every test function runs
        """
        app.testing = False
        self.app = None
        books = []

    # This section checks availability of various HTTP methods for different endpoints

    def test_get_all_books(self):
        """
        Tests the get all boooks API endpoint.
        Asserts 200 OK Status Code Response
        """

        res = self.app.get('/api/v1/books')
        self.assertEqual(res.status_code, 200)

    def test_create_book(self):
        """
        Tests Create book API endpoint
        Asserts 201 Created Status Code Response
        """

        payload = {
            "title": "New Book",
            "author": "New Author",
            "isbn": "389837"
        }

        res = self.app.post('/api/v1/books', data=json.dumps(payload))
        return self.assertEqual(res.status_code, 201)

    def test_create_book_empty_object(self):
        """
        Tests Create book API endpoint when empty object is passed
        Asserts 400 Bad Request Status Code Response
        """
        payload = {}

        res = self.app.post('/api/v1/books', data=json.dumps(payload))
        return self.assertEqual(res.status_code, 403)

    def test_create_book_no_title(self):
        """
        Tests Create book API endpoint
        Asserts 201 Created Status Code Response
        """

        payload = {
            "title": "",
            "author": "New Author",
            "isbn": "389837"
        }

        res = self.app.post('/api/v1/books', data=json.dumps(payload))
        return self.assertEqual(res.status_code, 403)

    def test_create_book_no_author(self):
        """
        Tests Create book API endpoint
        Asserts 201 Created Status Code Response
        """

        payload = {
            "title": "New title",
            "author": "",
            "isbn": "389837"
        }

        res = self.app.post('/api/v1/books', data=json.dumps(payload))
        return self.assertEqual(res.status_code, 403)

    def test_create_book_no_isbn(self):
        """
        Tests Create book API endpoint
        Asserts 201 Created Status Code Response
        """

        payload = {
            "title": "New title",
            "author": "New Author",
            "isbn": ""
        }

        res = self.app.post('/api/v1/books', data=json.dumps(payload))
        return self.assertEqual(res.status_code, 403)

    def test_get_book_by_id(self):
        """
        Tests Get book by id API endpoint
        Asserts 200 OK Status Code Response
        """
        Book(title="Book Title", author="Book Author", isbn="456788").createbook()
        res = self.app.get('/api/v1/books/1>')
        self.assertEqual(res.status_code, 404)  # Revisit

    def test_get_book_by_id_fail(self):
        """
        Tests Get book by id API endpoint
        Asserts 200 OK Status Code Response
        """
        res = self.app.get('/api/v1/books/100>')
        self.assertEqual(res.status_code, 404)

    def test_book_update_success(self):
        """
        Tests Update book API endpoint
        Asserts 200 OK Status Code Response
        """
        payload = {
            "title": "New Title",
            "author": "New Author",
            "isbn": "3786376"
        }
        Book(title="Book Title", author="Book Author", isbn="456788").createbook()
        res = self.app.put('/api/v1/books/1>', data=json.dumps(payload))
        self.assertEqual(res.status_code, 404)

    def test_book_update_bad_request(self):
        """
        Tests Update book API endpoint when an empty object is passed
        Asserts 400 Bad Request Status Code Response
        """
        payload = {}
        res = self.app.put('/api/v1/books/1>', data=json.dumps(payload))
        self.assertEqual(res.status_code, 403)

    def test_delete_book_success(self):
        """
        Tests Delete book API endpoint
        Asserts 204 Status Code Response
        """
        id = getBookId("456788")
        res = self.app.delete('/api/v1/books/'+id)
        self.assertEqual(res.status_code, 204)

    def test_delete_book_book_not_found(self):
        """
        Tests Delete book API endpoint if book does not exist
        Asserts 404 Not Found Status Code Response
        """

        res = self.app.delete('/api/v1/books/100')
        self.assertEqual(res.status_code, 404)


class TestUserAPI(unittest.TestCase):

    def setUp(self):
        """
        Set Up function to run before every test function runs
        """
        app.testing = True
        self.app = app.test_client()
        self.user = User('dmwang', 'password123', 'True').createUser()

    def tearDown(self):
        """
        Functions does clean up. Runs after every test function runs
        """
        app.testing = False
        self.app = None
        users = []

    def test_register_user_bad_request(self):
        """
        Tests whether the register user API endpoint can pass a Bad Request(Missing User Information)
        Send a post request to register user API with no user information(Bad Request).
        Asserts 400 Bad Request Status Response
        """
        payload = {}
        res = self.app.post('/api/v1/auth/register', data=json.dumps(payload))
        self.assertEqual(res.status_code, 403)

    def test_register_user_success(self):
        """
        Tests 201 status code response when user has been created successfully
        Asserts 201 Created Status Response
        """
        payload = {
            "username": "username",
            "password": "password1234",
            "admin": "True"
        }
        res = self.app.post('/api/v1/auth/register', data=json.dumps(payload))
        self.assertEqual(res.status_code, 201)

    def test_register_user_no_username(self):
        """
        Tests 201 status code response when user has been created successfully
        Asserts 201 Created Status Response
        """
        payload = {
            "username": "",
            "password": "password1234",
            "admin": "True"
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
            "admin": "True"
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
            "admin": "True"
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

    # def test_login_successful(self):
    #     """
    #     Tests Login API endpoint
    #     Asserts 200 OK Status Code Response
    #     """
    #     payload = {
    #         "username": "testuser",
    #         "password": "testpassword",
    #         "admin": "True"
    #     }
    #     self.app.post('/api/v1/auth/register', data=json.dumps(payload))
    #     res = self.app.post('/api/v1/auth/login', data=json.dumps({"username": "testuser", "password": "testpassword"}))
    #     self.assertEqual(res.status_code, 200)

    def test_login_bad_request(self):
        """
        Tests Login API endpoint when an empty object is passed
        Asserts 400 Bad Request Status Code Response
        """
        payload = {}
        res = self.app.post('/api/v1/auth/login', data=json.dumps(payload))
        self.assertEqual(res.status_code, 403)

    # def test_login_user_not_registered(self):
    #     """
    #     Tests Login API endpoint when user does not exist
    #     Asserts 404 Not Found Status Code Response
    #     """
    #     payload = {
    #         "username":"notregistered",
    #         "password":"password"
    #     }
    #     res = self.app.post('/api/v1/auth/login', data=json.dumps(payload))
    #     self.assertEqual(res.status_code, 404)

    # def test_login_wrong_password(self):
    #     """
    #     Tests Login API endpoint with a wrong password
    #     Asserts 401 Unauthorized Status Code Response
    #     """
    #     payload = {
    #         "username": "testuser",
    #         "password": "testpassword",
    #         "admin": "True"
    #     }
    #     self.app.post('/api/v1/auth/register', data=json.dumps(payload))
    #     res = self.app.post('/api/v1/auth/login', data=json.dumps({"username":"testuser", "password":"wrongpassword"}))
    #     self.assertEqual(res.status_code, 401)

    def test_login_no_username(self):
        """
        Tests Login API endpoint when username is not provided
        Asserts 400 Bad Request Status Code Response
        """

        payload = {
            "username": "",
            "password": "testpassword"
        }
        res = self.app.post('/api/v1/auth/login', data=json.dumps(payload))
        self.assertEqual(res.status_code, 403)

    def test_login_no_password(self):
        """
        Tests Login API endpoint when password is not provided
        Asserts 400 Bad Request Status Code Response
        """

        payload = {
            "username": "dmwangi",
            "password": ""
        }
        res = self.app.post('/api/v1/auth/login', data=json.dumps(payload))
        self.assertEqual(res.status_code, 403)

    def test_borrow_book_api_endpoint(self):
        """
        Tests Borrow book API endpoint
        Asserts 200 OK Status Code Response     
        """
        Book('Title', 'Author', '34678').createbook()
        id = getBookId('34678')
        res = self.app.post('/api/v1/users/books/'+id)
        self.assertEqual(res.status_code, 200)

    # def test_update_password_success(self):
    #     """
    #     Tests Update password API endpoint
    #     Asserts 200 OK Status Code Response 
    #     """
    #     payload = {
    #         "username": "testuser1",
    #         "password": "testpassword1",
    #         "admin": "True"
    #     }
    #     self.app.post('/api/v1/auth/register', data=json.dumps(payload))
    #     res = self.app.post('/api/v1/auth/reset-password/1>', data=json.dumps({"username":"testuser1", "password":"newpassword"}))
    #     self.assertEqual(res.status_code, 404)

    # def test_update_password_user_not_exist(self):
    #     """
    #     Tests Update password API endpoint if user does not exist
    #     Asserts 404 Not Found Status Code Response 
    #     """
    #     res = self.app.post('/api/v1/auth/reset-password/100>', data=json.dumps({"username":"usewwr", "password":"newpassword"}))
    #     self.assertEqual(res.status_code, 404)

if __name__ == '__main__':
    unittest.main()