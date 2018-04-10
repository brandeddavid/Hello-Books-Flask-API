import unittest
import json
from api.models import Book, User
from api.bkendlogic import getBookId, deleteAllBooks
from run import app
from flask import jsonify
from api import users, books


class TestBookAPI(unittest.TestCase):

    def setUp(self):
        """
        Set Up function to run before every test function runs
        """

        app.testing = True
        self.app = app.test_client()
        self.book = Book(title="Book Title", author="Book Author", isbn="456788")
        books[self.book.id] = self.book.__dict__

    def tearDown(self):
        """
        Functions does clean up. Runs after every test function runs
        """
        app.testing = False
        self.app = None

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

    def test_create_book_empty_title(self):
        """
        Tests Create book API endpoint
        Asserts 201 Created Status Code Response
        """
        payload = {
            "title": "   ",
            "author": "New Author",
            "isbn": "4647689"
        }
        res = self.app.post('/api/v1/books', data=json.dumps(payload))
        return self.assertEqual(res.status_code, 403)

    def test_create_book_empty_author(self):
        """
        Tests Create book API endpoint
        Asserts 201 Created Status Code Response
        """
        payload = {
            "title": "New Title",
            "author": "     ",
            "isbn": ""
        }
        res = self.app.post('/api/v1/books', data=json.dumps(payload))
        return self.assertEqual(res.status_code, 403)

    def test_create_book_empty_isbn(self):
        """
        Tests Create book API endpoint
        Asserts 201 Created Status Code Response
        """
        payload = {
            "title": "New Title",
            "author": "New Author",
            "isbn": "     "
        }
        res = self.app.post('/api/v1/books', data=json.dumps(payload))
        return self.assertEqual(res.status_code, 403)

    def test_create_book_already_exists(self):
        """
        Tests Create book API endpoint
        Asserts 409 Created Status Code Response
        """
        payload = {
            "title": "Book Title1", 
            "author": "Book Author1", 
            "isbn": "456788"
        }
        res = self.app.post('/api/v1/books', data=json.dumps(payload))
        return self.assertEqual(res.status_code, 409)

    def test_get_book_by_id(self):
        """
        Tests Get book by id API endpoint
        Asserts 200 OK Status Code Response
        """
        id = getBookId("456788")
        res = self.app.get('/api/v1/books/' +id)
        self.assertEqual(res.status_code, 200)  # Revisit

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
        id = getBookId("456788")
        res = self.app.put('/api/v1/books/' +id, data=json.dumps(payload))
        self.assertEqual(res.status_code, 200)

    def test_book_update_bad_request(self):
        """
        Tests Update book API endpoint when an empty object is passed
        Asserts 400 Bad Request Status Code Response
        """
        payload = {}
        id = getBookId("456788")
        res = self.app.put('/api/v1/books/' +id, data=json.dumps(payload))
        self.assertEqual(res.status_code, 403)

    def test_book_update_no_title(self):
        """
        Tests Update book API endpoint when an empty object is passed
        Asserts 400 Bad Request Status Code Response
        """
        payload = {
            "title": "",
            "author": "New Author",
            "isbn": "3786376"
        }
        id = getBookId("456788")
        res = self.app.put('/api/v1/books/' +id, data=json.dumps(payload))
        self.assertEqual(res.status_code, 403)

    def test_book_update_no_author(self):
        """
        Tests Update book API endpoint when an empty object is passed
        Asserts 400 Bad Request Status Code Response
        """
        payload = {
            "title": "New Title",
            "author": "",
            "isbn": "3786376"
        }
        id = getBookId("456788")
        res = self.app.put('/api/v1/books/' +id, data=json.dumps(payload))
        self.assertEqual(res.status_code, 403)

    def test_book_update_no_isbn(self):
        """
        Tests Update book API endpoint when an empty object is passed
        Asserts 400 Bad Request Status Code Response
        """
        payload = {
            "title": "New Title",
            "author": "New Title",
            "isbn": ""
        }
        id = getBookId("456788")
        res = self.app.put('/api/v1/books/' +id, data=json.dumps(payload))
        self.assertEqual(res.status_code, 403)

    def test_book_update_not_exist(self):
        """
        Tests Update book API endpoint
        Asserts 200 OK Status Code Response
        """
        payload = {
            "title": "New Title",
            "author": "New Author",
            "isbn": "3786376"
        }
        res = self.app.put('/api/v1/books/1000', data=json.dumps(payload))
        self.assertEqual(res.status_code, 404)

    def test_delete_book_success(self):
        """
        Tests Delete book API endpoint
        Asserts 204 Status Code Response
        """
        id = getBookId("456788")
        res = self.app.delete('/api/v1/books/'+id)
        self.assertEqual(res.status_code, 204)
        print(books)

    def test_delete_book_book_not_found(self):
        """
        Tests Delete book API endpoint if book does not exist
        Asserts 404 Not Found Status Code Response
        """
        res = self.app.delete('/api/v1/books/100')
        self.assertEqual(res.status_code, 404)

if __name__ == '__main__':
    unittest.main()