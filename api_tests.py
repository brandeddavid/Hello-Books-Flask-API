import unittest
from api.models import *
from run import app
from flask import jsonify



# class Testcreateuser(unittest.TestCase):
#
#     def setUp(self):
#         self.app = app.app.test_client()
#         self.user = Users('David', 'Mwangi','dmwangi', 'password123')
#
#     def test_api_exists(self):
#
#         res = self.app.get('/api/v1/auth/register')
#         self.assertEqual(res.status_code, 200)


class TestBookAPI(unittest.TestCase):

    def setUp(self):

        app.testing = True
        self.app = app.test_client()
        self.book = Book.apicreatebook(id='6', data={'title': 'Hello Children', 'author': 'Tom Chris', 'isbn': '38561993'})
        update = {'title': 'Tom and Mary', 'author': 'Tom Chris', 'isbn': '38561993'}

    def tearDown(self):

        pass

    # This section checks availability of various HTTP methods for different endpoints

    def test_get_method_exists_for_get_all_books(self):

        res = self.app.get('/api/v1/books')
        self.assertEqual(res.status_code, 200)

    def test_get_method_for_get_a_book_api(self):

        res = self.app.get('/api/v1/books/<string:book_id>')
        self.assertEqual(res.status_code, 200)


    def test_delete_method_for_delete_a_book_api(self):
        res = self.app.delete('/api/v1/books/<string:book_id>')
        self.assertEqual(res.status_code, 200)


    def test_get_all_books(self):

        res = self.app.get('/api/v1/books')
        self.assertIn('Hello Children', str(res.data))

    def test_get_book_by_id(self):
        pass
        # res = self.app.get('/api/v1/books/<string:book_id>')
        # self.assertIn('Hello Children', str(res.data))

    def test_book_update(self):
        res = self.app.put('/api/v1/books/<string:book_id>')


if __name__ == "__main__":
    unittest.main()
