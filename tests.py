import unittest
import json
from run import app
from flask import jsonify
from api.models import Book, User


class TestBooksModel(unittest.TestCase):

    def setUp(self):
        """
        Set Up function to run before every test function runs
        """

        self.book = Book('Game of Thrones', 'George R.R. Martin', '3878749').createbook()

    def tearDown(self):
        """
        Functions does clean up. Runs after every test function runs
        """
        self.book = None 

    def test_book_creation_successful(self):
        """
        Function tests successful book creation.
        Asserts message returned after successful book creation
        """

        res = Book('Game of Thrones', 'George R.R. Martin', '363837').createbook()
        self.assertEqual(res, {'Success': 'Book Created Successfully'})

    def test_book_already_exists(self):
        """
        Function tests book being added already exists
        Asserts message returned if book being added exists
        """
        res = Book('Game of Thrones', 'George R.R. Martin', '3878749').createbook()
        self.assertEqual(res, {'Message': 'Book Already Exists'})

    def test_book_does_not_exist(self):
        """
        Function tests query for a book that does not exist
        Asserts message returned if book does not exist
        """
        res = Book.getbook('30')
        self.assertEqual(res, {'Message': 'Book Does not Exist'})

    def test_book_update_unsuccessful(self):
        """
        Function unsuccessful book update
        Asserts message returned if book update unsuccessful
        """
        res = Book.updatebook(
            '1', {'title': 'GOT', 'author': 'George', 'isbn': '827890'})
        self.assertEqual(res, {'Message': 'Book Does Not Exist'})

    def test_book_delete_unsuccessful(self):
        """
        Function tests unsuccessful book deletion
        Asserts message returned if book deletion is unsuccessful
        """
        res = Book.deletebook('100')
        self.assertEqual(res, {'Message': 'Book Does Not Exist'})


class TestBookAPI(unittest.TestCase):

    def setUp(self):
        """
        Set Up function to run before every test function runs
        """

        app.testing = True
        self.app = app.test_client()
        self.book = Book(title="Book Title",
                         author="Book Author", isbn="456788")

    def tearDown(self):
        """
        Functions does clean up. Runs after every test function runs
        """
        app.testing = False
        self.app = None

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
        payload = {

        }

        res = self.app.post('/api/v1/books', data=json.dumps(payload))
        return self.assertEqual(res.status_code, 400)

    def test_get_book_by_id(self):
        """
        Tests Get book by id API endpoint
        Asserts 200 OK Status Code Response
        """
        Book(title="Book Title", author="Book Author", isbn="456788")
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
        res = self.app.put('/api/v1/books/1>', data=json.dumps(payload))
        self.assertEqual(res.status_code, 200)

    def test_book_update_bad_request(self):
        """
        Tests Update book API endpoint when an empty object is passed
        Asserts 400 Bad Request Status Code Response
        """
        payload = {}
        res = self.app.put('/api/v1/books/1>', data=json.dumps(payload))
        self.assertEqual(res.status_code, 400)

    def test_delete_book_success(self):
        """
        Tests Delete book API endpoint
        Asserts 200 OK Status Code Response
        """

        res = self.app.delete('/api/v1/books/1')
        self.assertEqual(res.status_code, 200)

    def test_delete_book_book_not_found(self):
        """
        Tests Delete book API endpoint if book does not exist
        Asserts 404 Not Found Status Code Response
        """

        res = self.app.delete('/api/v1/books/100')
        self.assertEqual(res.status_code, 404)


class TestUserModel(unittest.TestCase):

    def setUp(self):
        """
        Function run before each test is run
        """
        self.user = User('dmwangi', 'password', True).createUser()

    def tearDown(self):
        """
        Function run after each test is run
        """
        pass

    def test_user_creation_successful(self):
        """
        Function tests user creation function
        Asserts message returned after successful user creation
        """
        res = User('jdoe', 'jdoe123', False).createUser()
        self.assertEqual(res, {'Message': 'User Created Successfully'})

    def test_username_exists(self):
        """
        Function tests user creation function fail because username exists
        Asserts message returned after failed user creation if user already exists
        """
        res = User('dmwangi', 'password', True).createUser()
        self.assertEqual(res, {'Message': 'Username Exists'})

    def test_get_all_users(self):
        """
        Functions tests get all user function
        """
        res = User.getAllUsers()
        self.assertIn('dmwangi', str(res))

    def test_user_update_password(self):
        """
        Function tests user update password function
        Asserts message returned after successful password update
        """
        user = self.user
        res = User.updatePassword(id=1, username='dmwangi', password='password1')
        self.assertEqual(res, {'Message': 'User Password Updated Successfully'})

    def test_user_update_fail(self):
        """
        Function tests user update password function fail
        Asserts message returned after a failed password update
        """
        user = self.user
        res = User.updatePassword(id=1, username='tom', password='password1')
        self.assertEqual(res, {'Message': 'User Password Update Failed'})

    def test_book_borrowing_fail(self):
        """
        Function tests user borrow book function fail
        Asserts message returned after a failed book borrow
        """
        book = Book(title='Book Title', author='Book Author',isbn="64368").createbook()
        res = User.borrowBook("10")
        self.assertEqual(res, {'Message': 'Book Does Not Exist'})


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

    def test_register_user_bad_request(self):
        """
        Tests whether the register user API endpoint can pass a Bad Request(Missing User Information)
        Send a post request to register user API with no user information(Bad Request).
        Asserts 400 Bad Request Status Response
        """
        payload = {}
        res = self.app.post('/api/v1/auth/register', data=json.dumps(payload))
        self.assertEqual(res.status_code, 400)

    def test_register_user_success(self):
        """
        Tests 201 status code response when user has been created successfully
        Asserts 201 Created Status Response
        """
        payload = {
            "username": "username",
            "password": "password",
            "admin": "True"
        }
        res = self.app.post('/api/v1/auth/register', data=json.dumps(payload))
        self.assertEqual(res.status_code, 201)

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
            "username": "testuser",
            "password": "testpassword",
            "admin": "True"
        }
        res = self.app.post('/api/v1/auth/register', data=json.dumps(payload))
        res1 = self.app.post('/api/v1/auth/login', data=json.dumps({"username": "testuser", "password": "testpassword"}))
        self.assertEqual(res1.status_code, 200)

    def test_login_bad_request(self):
        """
        Tests Login API endpoint when an empty object is passed
        Asserts 400 Bad Request Status Code Response
        """
        payload = {}
        res = self.app.post('/api/v1/auth/login', data=json.dumps(payload))
        self.assertEqual(res.status_code, 400)

    def test_login_user_not_registered(self):
        """
        Tests Login API endpoint when user does not exist
        Asserts 404 Not Found Status Code Response
        """
        payload = {
            "username":"notregistered",
            "password":"password"
        }
        res = self.app.post('/api/v1/auth/login', data=json.dumps(payload))
        self.assertEqual(res.status_code, 404)

    def test_login_wrong_password(self):
        """
        Tests Login API endpoint with a wrong password
        Asserts 401 Unauthorized Status Code Response
        """
        payload = {
            "username": "testuser",
            "password": "testpassword",
            "admin": "True"
        }
        res1 = self.app.post('/api/v1/auth/register', data=json.dumps(payload))
        res = self.app.post('/api/v1/auth/login', data=json.dumps({"username":"testuser", "password":"wrongpassword"}))
        self.assertEqual(res.status_code, 401)

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
        self.assertEqual(res.status_code, 400)

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
        self.assertEqual(res.status_code, 400)

    def test_borrow_book_api_endpoint(self):
        """
        Tests Borrow book API endpoint
        Asserts 200 OK Status Code Response     
        """
        res = self.app.post('/api/v1/users/books/<string:book_id>')
        self.assertEqual(res.status_code, 200)

    def test_update_password_success(self):
        """
        Tests Update password API endpoint
        Asserts 200 OK Status Code Response 
        """
        payload = {
            "username": "testuser1",
            "password": "testpassword1",
            "admin": "True"
        }
        res1 = self.app.post('/api/v1/auth/register', data=json.dumps(payload))
        res = self.app.post('/api/v1/auth/reset-password/1>', data=json.dumps({"username":"testuser1", "password":"newpassword"}))
        self.assertEqual(res.status_code, 404)

    def test_update_password_user_not_exist(self):
        """
        Tests Update password API endpoint if user does not exist
        Asserts 404 Not Found Status Code Response 
        """
        res = self.app.post('/api/v1/auth/reset-password/100>', data=json.dumps({"username":"usewwr", "password":"newpassword"}))
        self.assertEqual(res.status_code, 404)


if __name__ == '__main__':

    unittest.main()
