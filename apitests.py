import unittest
import sys
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
        self.user = User(1, 'dmwangi', 'password123').createUser()

    def tearDown(self):
        """

        :return:
        """
        app.testing = False

    def test_user_registration_api_exists(self):
        """

        :return:
        """
        res = self.app.get('/api/v1/auth/register')
        self.assertEqual(res.status_code, 200)

    def test_get_all_user_api_exits(self):
        """

        :return:
        """
        res = self.app.get('/api/v1/users')
        self.assertEqual(res.status_code, 200)

    def test_user_login_api_exists(self):
        """

        :return:
        """
        res = self.app.post('/api/v1/auth/login')
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


class TestBookAPI(unittest.TestCase):

    def setUp(self):
        """

        :return:
        """

        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        """

        :return:
        """
        app.testing = False

    # This section checks availability of various HTTP methods for different endpoints

    def test_get_method_exists_for_get_all_books(self):
        """

        :return:
        """

        res = self.app.get('/api/v1/books')
        self.assertEqual(res.status_code, 200)

    def test_get_method_for_get_a_book_api(self):
        """

        :return:
        """

        res = self.app.get('/api/v1/books/<string:book_id>')
        self.assertEqual(res.status_code, 200)

    def test_delete_method_for_delete_a_book_api(self):
        """

        :return:
        """
        res = self.app.delete('/api/v1/books/<string:book_id>')
        self.assertEqual(res.status_code, 200)

    def test_get_all_books(self):
        """

        :return:
        """

        res = self.app.get('/api/v1/books')
        self.assertIn('Hello Children', str(res.data))

    def test_get_book_by_id(self):
        """

        :return:
        """
        pass
        # res = self.app.get('/api/v1/books/<string:book_id>')
        # self.assertIn('Hello Children', str(res.data))

    def test_book_update(self):
        """

        :return:
        """
        res = self.app.put('/api/v1/books/<string:book_id>')


if __name__ == "__main__":
    unittest.main()
