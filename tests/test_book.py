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

    def test_add_book(self):
        empty_book =self.add_book(self.empty_book_data)
        self.assertEqual(empty_book.status_code, 403)
        no_title = self.add_book(self.book_data_no_title)
        self.assertEqual(no_title.status_code, 403)
        no_author = self.add_book(self.book_data_no_author)
        self.assertEqual(no_author.status_code, 403)
        no_isbn = self.add_book(self.book_data_no_isbn)
        self.assertEqual(no_isbn.status_code, 403)
        no_publisher = self.add_book(self.book_data_no_publisher)
        self.assertEqual(no_publisher.status_code, 403)
        add_book = self.add_book(self.book_data)
        self.assertEqual(add_book.status_code, 201)
