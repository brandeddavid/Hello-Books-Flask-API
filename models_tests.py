import unittest
from models import *


class TestBooksModel(unittest.TestCase):

    def setUp(self):
        self.book = Book()
        self.book.createbook('1', 'Game of Thrones', 'George R.R. Martin')

    def tearDown(self):
        pass

    def test_book_creation_successful(self):

        res = self.book.createbook('2', 'Game of Thrones', 'George R.R. Martin')
        self.assertEqual(res, 'Book Created Successfully')

    def test_book_already_exists(self):
        res = self.book.createbook('1', 'Game of Thrones', 'George R.R. Martin')
        self.assertEqual(res, 'Book Already Exists')

    def test_book_exists(self):
        res = self.book.getbook('1')
        self.assertEqual(res, 'Book Exists')

    def test_book_does_not_exist(self):
        res = self.book.getbook('3')
        self.assertEqual(res, 'Book Does not Exist')

    def test_book_delete_successful(self):
        res = self.book.deletebook('1')
        self.assertEqual(res, 'Book Deleted Successfully')

    def test_book_update_successful(self):
        res = self.book.updatebook('1', 'GOT', 'George')
        self.assertEqual(res, 'Book Update Successful')


class TestUserModel(unittest.TestCase):

    def setUp(self):
        self.user = User()
        self.user.createUser('David', 'Mwangi', 'dmwangi', 'password')

    def tearDown(self):
        pass

    def test_user_creation_successful(self):
        res = self.user.createUser('David', 'Mwangi', 'geekdave', 'password')
        self.assertEqual(res, 'User Created Successfully')

    def test_user_already_exists(self):
        res = self.user.createUser('David', 'Mwangi', 'dmwangi', 'password')
        self.assertEqual(res, 'User Already Exists')

    def test_user_login(self):
        res = self.user.loginUser('dmwangi', 'password')
        self.assertEqual(res, 'User Login Successful')

    def test_user_does_not_exist(self):
        pass

    def test_password_mismatch(self):
        pass

    def test_user_update_password(self):
        res = self.user.updatePassword('dmwangi', 'password', 'newpassword')
        self.assertEqual(res, 'Password Reset Successful')

    def test_user_update_password_user_not_exist(self):
        pass

    def test_user_update_password_mismatch(self):
        pass

    def test_delete_user(self):
        res = self.user.deleteUser('dmwangi')
        self.assertEqual(res, 'User Deleted Successfully')

    def test_book_borrowing(self):
        res = self.user.borrowBook('dmwangi', 'password', '1')
        self.assertEqual(res, 'Book Borrowed Successfully')


if __name__ == '__main__':

    unittest.main()
