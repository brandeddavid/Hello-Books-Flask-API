from tests.base_test import TestHelloBooks
import json


class AuthTestCase(TestHelloBooks):
    """[summary]
    
    Arguments:
        TestHelloBooks {[type]} -- [description]
    """

    def test_registration(self):
        register = self.register_user(self.user_data)
        self.assertEqual(register.status_code, 201)
        empty_data = self.register_user(self.empty_user_data)
        self.assertEqual(empty_data.status_code, 403)
