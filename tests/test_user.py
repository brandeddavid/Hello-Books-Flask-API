from tests.base_test import TestHelloBooks
import json

class UserTestCase(TestHelloBooks):

    def test_get_users(self):
        self.register_user(self.user_data)
        all_users = self.get_all_users()
        self.assertEqual(all_users.status_code, 200)

    def test_borrow_book(self):
        no_book = self.borrow_book(1)
        self.assertEqual(no_book.status_code, 404)
        self.add_book(self.book_data)
        # book = self.borrow_book(10)
        # self.assertEqual(book.status_code, 200)
