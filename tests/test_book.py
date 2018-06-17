from tests.base_test import TestHelloBooks
import json

class BookTestCase(TestHelloBooks):
    """[summary]
    
    Arguments:
        TestHelloBooks {[type]} -- [description]
    """

    def test_get_books(self):
        no_books = self.get_all_books()
        self.assertEqual(no_books.status_code, 404)
        no_book = self.get_book(1000)
        self.assertEqual(no_book.status_code, 404)
        bad_argument = self.get_book('kk')
        self.assertEqual(bad_argument.status_code, 403)
