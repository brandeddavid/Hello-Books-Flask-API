import unittest
from api.models import Book, User


class TestBooksModel(unittest.TestCase):

    def setUp(self):
        """

        :return:
        """
        self.book = Book('Game of Thrones', 'George R.R. Martin', '3878749').createbook()

    def tearDown(self):
        """

        :return:
        """
        pass

    def test_book_creation_successful(self):
        """

        :return:
        """

        res = Book('Game of Thrones', 'George R.R. Martin', '363837').createbook()
        self.assertEqual(res, {'Success': 'Book Created Successfully'})

    def test_book_already_exists(self):
        """

        :return:
        """
        res = Book('Game of Thrones', 'George R.R. Martin', '3878749').createbook()
        self.assertEqual(res, {'Message': 'Book Already Exists'})

    def test_book_does_not_exist(self):
        """

        :return:
        """
        res = Book.getbook('30')
        self.assertIn({'Message': 'Book Does not Exist'}, res)

    def test_book_update_successful(self):
        """

        :return:
        """
        res = Book.updatebook('1', {'title':'GOT', 'author':'George', 'isbn':'827890'})
        self.assertEqual(res, {'Message': 'Book Update Successful'})

    def test_book_update_unsuccessful(self):
        """

        :return:
        """
        res = Book.updatebook('1', {'title':'GOT', 'author':'George', 'isbn':'827890'})
        self.assertEqual(res, {'Message': 'Book Does Not Exist'})

    def test_book_delete_successful(self):
        """

        :return:
        """
        res = Book.deletebook('1')
        self.assertEqual(res, {'Message': 'Book Deleted Successfully'})
        
    def test_book_delete_unsuccessful(self):
        """

        :return:
        """
        res = Book.deletebook('100')
        self.assertEqual(res, {'Message': 'Book Does Not Exist'})


class TestUserModel(unittest.TestCase):

    def setUp(self):
        """
        Function run before each test is run
        :return:
        """
        self.user = User(1, 'dmwangi', 'password', True).createUser()

    def tearDown(self):
        """
        Function run after each test is run
        :return:
        """
        pass

    def test_user_creation_successful(self):
        """
        Function tests user creation function
        :return:
        """
        res = User(2, 'jdoe', 'jdoe123', False).createUser()
        self.assertEqual(res, {'Message': 'User Created Successfully'})

    def test_user_id_exists(self):
        """

        :return:
        """
        res = User(1, 'dmwangi', 'password', True).createUser()
        self.assertEqual(res, {'Message': 'User id Exists'})

    def test_username_exists(self):
        """

        :return:
        """
        res = User(3, 'dmwangi', 'password', True).createUser()
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
