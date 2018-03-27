import unittest
from api.models import *


class TestBooksModel(unittest.TestCase):

    def setUp(self):
        """

        :return:
        """
        self.book = Book()
        self.book.createbook('1', 'Game of Thrones', 'George R.R. Martin')

    def tearDown(self):
        """

        :return:
        """
        pass

    def test_book_creation_successful(self):
        """

        :return:
        """

        res = self.book.createbook('2', 'Game of Thrones', 'George R.R. Martin')
        self.assertEqual(res, 'Book Created Successfully')

    def test_book_already_exists(self):
        """

        :return:
        """
        res = self.book.createbook('1', 'Game of Thrones', 'George R.R. Martin')
        self.assertEqual(res, 'Book Already Exists')

    def test_book_exists(self):
        """

        :return:
        """
        res = self.book.getbook('1')
        self.assertEqual(res, 'Book Exists')

    def test_book_does_not_exist(self):
        """

        :return:
        """
        res = self.book.getbook('3')
        self.assertEqual(res, 'Book Does not Exist')

    def test_book_delete_successful(self):
        """

        :return:
        """
        res = self.book.deletebook('1')
        self.assertEqual(res, 'Book Deleted Successfully')

    def test_book_update_successful(self):
        """

        :return:
        """
        res = self.book.updatebook('1', 'GOT', 'George')
        self.assertEqual(res, 'Book Update Successful')


class TestUserModel(unittest.TestCase):

    def setUp(self):
        """

        :return:
        """
        self.user = User(1, 'dmwangi', 'password').createUser()

    def tearDown(self):
        """

        :return:
        """
        pass

    def test_user_creation_successful(self):
        """

        :return:
        """
        res = User(2, 'jdoe', 'jdoe123').createUser()
        self.assertEqual(res, {'Message': 'User Created Successfully'})

    def test_user_id_exists(self):
        """

        :return:
        """
        res = User(1, 'dmwangi', 'password').createUser()
        self.assertEqual(res, {'Message': 'User id Exists'})

    def test_username_exists(self):
        """

        :return:
        """
        res = User(3, 'dmwangi', 'password').createUser()
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
        res = User.updatePassword(id=1, username='dmwangi', password='password1')
        self.assertEqual(res, {'Message': 'User Password Updated Successfully'})

    def test_user_update_fail(self):
        """

        :return:
        """
        user = self.user
        res = User.updatePassword(id=1, username='tom', password='password1')
        self.assertEqual(res, {'Message': 'User Password Update Failed'})

    def test_book_borrowing(self):
        """

        :return:
        """
        book = Book(title='Book Title', author='Book Author', isbn="64368").createbook()
        res = User.borrowBook("1")
        self.assertEqual(res, {'Message': 'Successfully Borrowed Book'})

    def test_book_borrowing_fail(self):
        """

        :return:
        """
        book = Book(title='Book Title', author='Book Author', isbn="64368").createbook()
        res = User.borrowBook("10")
        self.assertEqual(res, {'Message': 'Book Does Not Exist'})

if __name__ == '__main__':

    unittest.main()
