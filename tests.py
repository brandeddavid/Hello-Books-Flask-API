import unittest
import json
from run import app
from flask import jsonify
from api.models import Book, User


class TestBooksModel(unittest.TestCase):

    def setUp(self):
        """

        :return:
        """
        self.book = Book('Game of Thrones',
                         'George R.R. Martin', '3878749').createbook()

    def tearDown(self):
        """

        :return:
        """
        pass

    def test_book_creation_successful(self):
        """

        :return:
        """

        res = Book('Game of Thrones', 'George R.R. Martin',
                   '363837').createbook()
        self.assertEqual(res, {'Success': 'Book Created Successfully'})

    def test_book_already_exists(self):
        """

        :return:
        """
        res = Book('Game of Thrones', 'George R.R. Martin',
                   '3878749').createbook()
        self.assertEqual(res, {'Message': 'Book Already Exists'})

    def test_book_does_not_exist(self):
        """

        :return:
        """
        res = Book.getbook('30')
        self.assertEqual(res, {'Message': 'Book Does not Exist'})

    def test_book_update_unsuccessful(self):
        """

        :return:
        """
        res = Book.updatebook(
            '1', {'title': 'GOT', 'author': 'George', 'isbn': '827890'})
        self.assertEqual(res, {'Message': 'Book Does Not Exist'})

    def test_book_delete_unsuccessful(self):
        """

        :return:
        """
        res = Book.deletebook('100')
        self.assertEqual(res, {'Message': 'Book Does Not Exist'})


class TestBookAPI(unittest.TestCase):

    def setUp(self):
        """

        :return:
        """

        app.testing = True
        self.app = app.test_client()
        self.book = Book(title="Book Title",
                         author="Book Author", isbn="456788")

    def tearDown(self):
        """

        :return:
        """
        app.testing = False
        self.app = None

    # This section checks availability of various HTTP methods for different endpoints

    def test_get_all_books(self):
        """
        Tests the get all boooks API endpoint.
        :return: 200 OK Status Code Response
        """

        res = self.app.get('/api/v1/books')
        self.assertEqual(res.status_code, 200)

    def test_create_book(self):
        """
        Tests Create book API endpoint
        :return: 201 Created Status Code Response
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
        :return:
        """
        payload = {

        }

        res = self.app.post('/api/v1/books', data=json.dumps(payload))
        return self.assertEqual(res.status_code, 400)

    def test_get_book_by_id(self):
        """

        :return:
        """
        Book(title="Book Title", author="Book Author", isbn="456788")
        res = self.app.get('/api/v1/books/1>')
        self.assertEqual(res.status_code, 404)  # Revisit

    def test_get_book_by_id_fail(self):
        """

        :return:
        """
        res = self.app.get('/api/v1/books/100>')
        self.assertEqual(res.status_code, 404)

    def test_book_update_success(self):
        """

        :return:
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

        :return:
        """
        payload = {

        }
        res = self.app.put('/api/v1/books/1>', data=json.dumps(payload))
        self.assertEqual(res.status_code, 400)

    def test_delete_book_success(self):
        """
        [summary]
        """

        res = self.app.delete('/api/v1/books/1')
        self.assertEqual(res.status_code, 200)

    def test_delete_book_book_not_found(self):
        """
        [summary]
        """

        res = self.app.delete('/api/v1/books/100')
        self.assertEqual(res.status_code, 404)


class TestUserModel(unittest.TestCase):

    def setUp(self):
        """
        Function run before each test is run
        :return:
        """
        self.user = User('dmwangi', 'password', True).createUser()

    def tearDown(self):
        """
        Function run after each test is run
        :return:
        """
        pass

    def test_user_creation_successful(self):
        """
        Function tests user creation function
        :return:
        """
        res = User('jdoe', 'jdoe123', False).createUser()
        self.assertEqual(res, {'Message': 'User Created Successfully'})

    def test_username_exists(self):
        """

        :return:
        """
        res = User('dmwangi', 'password', True).createUser()
        self.assertEqual(res, {'Message': 'Username Exists'})

    def test_get_all_users(self):
        """

        :return:
        """
        res = User.getAllUsers()
        self.assertIn('dmwangi', str(res))

    def test_user_update_password(self):
        """

        :return:
        """
        user = self.user
        res = User.updatePassword(
            id=1, username='dmwangi', password='password1')
        self.assertEqual(
            res, {'Message': 'User Password Updated Successfully'})

    def test_user_update_fail(self):
        """

        :return:
        """
        user = self.user
        res = User.updatePassword(id=1, username='tom', password='password1')
        self.assertEqual(res, {'Message': 'User Password Update Failed'})

    def test_book_borrowing_fail(self):
        """

        :return:
        """
        book = Book(title='Book Title', author='Book Author',
                    isbn="64368").createbook()
        res = User.borrowBook("10")
        self.assertEqual(res, {'Message': 'Book Does Not Exist'})


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
        payload = {}
        res = self.app.post('/api/v1/auth/register', data=json.dumps(payload))
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

    def test_get_all_users(self):
        """

        :return:
        """
        res = self.app.get('/api/v1/users')
        self.assertEqual(res.status_code, 200)

    def test_login_successful(self):
        """
        [summary]
        """
        payload = {
            "username": "username",
            "password": "password",
            "admin": "True"
        }
        res = self.app.post('/api/v1/auth/register', data=json.dumps(payload))
        res = self.app.post('/api/v1/auth/login', data=json.dumps(payload))
        self.assertEqual(res.status_code, 401)

    def test_login_bad_request(self):
        """
        [summary]
        """
        payload = {}
        res = self.app.post('/api/v1/auth/login', data=json.dumps(payload))
        self.assertEqual(res.status_code, 401)

    def test_login_user_not_registered(self):
        """
        [summary]
        """
        payload = {
            "username":"notregistered",
            "password":"password"
        }
        res = self.app.post('/api/v1/auth/login', data=json.dumps(payload))
        self.assertEqual(res.status_code, 401)

    def test_login_wrong_password(self):
        """
        [summary]
        """
        payload = {
            "username":"dmwangi",
            "password":"password"
        }
        res = self.app.post('/api/v1/auth/login', data=json.dumps(payload))
        self.assertEqual(res.status_code, 401)

    def test_borrow_book_api_endpoint(self):
        """

        :return:
        """
        res = self.app.post('/api/v1/users/books/<string:book_id>')
        self.assertEqual(res.status_code, 200)

    def test_update_password_success(self):
        """

        :return:
        """
        res = self.app.post('/api/v1/auth/reset-password/<string:user_id>')
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':

    unittest.main()
