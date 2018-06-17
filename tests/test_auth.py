from tests.base_test import TestHelloBooks
import json


class AuthTestCase(TestHelloBooks):
    """[summary]
    
    Arguments:
        TestHelloBooks {[type]} -- [description]
    """

    def test_registration(self):
        empty_data = self.register_user(self.empty_user_data)
        self.assertEqual(empty_data.status_code, 403)
        no_email = self.register_user(self.user_data_no_email)
        self.assertEqual(no_email.status_code, 403)
        wrong_email = self.register_user(self.user_data_wrong_email)
        self.assertEqual(wrong_email.status_code, 400)
        long_email = self.register_user(self.user_data_long_email)
        self.assertEqual(long_email.status_code, 403)
        no_username = self.register_user(self.user_data_no_username)
        self.assertEqual(no_username.status_code, 403)
        long_username = self.register_user(self.user_data_long_username)
        self.assertEqual(long_username.status_code, 403)
        no_firstname = self.register_user(self.user_data_no_first_name)
        self.assertEqual(no_firstname.status_code, 403)
        long_firstname = self.register_user(self.user_data_long_first_name)
        self.assertEqual(long_firstname.status_code, 403)
        no_lastname = self.register_user(self.user_data_no_last_name)
        self.assertEqual(no_lastname.status_code, 403)
        long_lastname = self.register_user(self.user_data_long_last_name)
        self.assertEqual(long_lastname.status_code, 403)
        no_password = self.register_user(self.user_data_no_password)
        self.assertEqual(no_password.status_code, 403)
        short_password = self.register_user(self.user_data_short_password)
        self.assertEqual(short_password.status_code, 400)
        register = self.register_user(self.user_data)
        self.assertEqual(register.status_code, 201)
        email_exists = self.register_user(self.user_data)
        self.assertEqual(email_exists.status_code, 409)
        username_exists = self.register_user(self.user_data2)
        self.assertEqual(username_exists.status_code, 409)
    
    def test_login(self):
        pass