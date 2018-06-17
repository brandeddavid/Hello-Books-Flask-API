from tests.base_test import TestHelloBooks
import json


class AuthTestCase(TestHelloBooks):
    """[summary]
    
    Arguments:
        TestHelloBooks {[type]} -- [description]
    """

    def test_registration(self):
        register = self.register_user()
        print(register)
        self.assertEqual(register.status_code, 201)
