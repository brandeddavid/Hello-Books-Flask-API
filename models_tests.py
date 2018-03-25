import unittest
from models import *


class TestBooksModel(unittest.TestCase):

    def setUp(self):
        self.book = Books()

    def tearDown(self):
        pass

    def test_book_creation_successful(self):

        res = self.book.createbook('1', 'Game of Thrones', 'George R.R. Martin')
        self.assertEqual(res, 'Book Created Successfully')

    def test_book_exists(self):
        res = self.book.getbook('1')
        self.assertEqual(res, 'Book Exists')

    def test_book_does_not_exist(self):
        res = self.book.getbook('1')
        self.assertEqual(res, 'Book Does not Exist')

    def test_book_delete_successful(self):
        res = self.book.deletebook('1')
        self.assertEqual(res, 'Book Deletion Successful')

    def test_book_update_successful(self):
        res = self.book.updatebook('1')
        self.assertEqual(res, 'Book Update Successful')


class TestUserModel(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass