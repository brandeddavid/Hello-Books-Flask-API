import unittest
import json
from run import app
from api.models import Book, User


class TestBooksModel(unittest.TestCase):

    def setUp(self):
        """
        Set Up function to run before every test function runs
        """

        self.book = Book('Game of Thrones',
                         'George R.R. Martin', '3878749').createbook()

    def tearDown(self):
        """
        Functions does clean up. Runs after every test function runs
        """
        self.book = None

    def test_book_creation_successful(self):
        """
        Function tests successful book creation.
        Asserts message returned after successful book creation
        """

        res = Book('Game of Thrones', 'George R.R. Martin',
                   '363837').createbook()
        self.assertEqual(res, {'Success': 'Book Created Successfully'})

    def test_book_already_exists(self):
        """
        Function tests book being added already exists
        Asserts message returned if book being added exists
        """
        res = Book('Game of Thrones', 'George R.R. Martin',
                   '3878749').createbook()
        self.assertEqual(res, {'Message': 'Book Already Exists'})

    def test_book_does_not_exist(self):
        """
        Function tests query for a book that does not exist
        Asserts message returned if book does not exist
        """
        res = Book.getbook('30')
        self.assertEqual(res, {'Message': 'Book Does not Exist'})

    def test_book_update_unsuccessful(self):
        """
        Function unsuccessful book update
        Asserts message returned if book update unsuccessful
        """
        res = Book.updatebook(
            '10', {'title': 'GOT', 'author': 'George', 'isbn': '827890'})
        self.assertEqual(res, {'Message': 'Book Does Not Exist'})

    def test_book_delete_unsuccessful(self):
        """
        Function tests unsuccessful book deletion
        Asserts message returned if book deletion is unsuccessful
        """
        res = Book.deletebook('100')
        self.assertEqual(res, {'Message': 'Book Does Not Exist'})


class TestUserModel(unittest.TestCase):

    def setUp(self):
        """
        Function run before each test is run
        """
        self.user = User('dmwangi', 'password', True).createUser()

    def tearDown(self):
        """
        Function run after each test is run
        """
        pass

    def test_user_creation_successful(self):
        """
        Function tests user creation function
        Asserts message returned after successful user creation
        """
        res = User('jdoe', 'jdoe123', False).createUser()
        self.assertEqual(res, {'Message': 'User Created Successfully'})

    def test_username_exists(self):
        """
        Function tests user creation function fail because username exists
        Asserts message returned after failed user creation if user already exists
        """
        res = User('dmwangi', 'password', True).createUser()
        self.assertEqual(res, {'Message': 'Username Exists'})

    def test_get_all_users(self):
        """
        Functions tests get all user function
        """
        res = User.getAllUsers()
        self.assertIn('dmwangi', str(res))

    def test_user_update_password(self):
        """
        Function tests user update password function
        Asserts message returned after successful password update
        """
        user = self.user
        res = User.updatePassword(
            id=1, username='dmwangi', password='password1')
        self.assertEqual(
            res, {'Message': 'User Password Updated Successfully'})

    def test_user_update_fail(self):
        """
        Function tests user update password function fail
        Asserts message returned after a failed password update
        """
        user = self.user
        res = User.updatePassword(id=1, username='tom', password='password1')
        self.assertEqual(res, {'Message': 'User Password Update Failed'})

    def test_book_borrowing_fail(self):
        """
        Function tests user borrow book function fail
        Asserts message returned after a failed book borrow
        """
        book = Book(title='Book Title', author='Book Author',
                    isbn="64368").createbook()
        res = User.borrowBook("10")
        self.assertEqual(res, {'Message': 'Book Does Not Exist'})


if __name__ == '__main__':
    unittest.main()
