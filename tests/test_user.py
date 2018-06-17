from tests.base_test import TestHelloBooks
import json

class AllUsersTestCase(TestHelloBooks):
    """[summary]
    
    Arguments:
        TestHelloBooks {[type]} -- [description]
    """

    def test_get_users(self):
        no_users = self.get_all_users()
        self.assertEquals(no_users.status_code, 200)
        self.register_user(self.user_data)
        all_users = self.get_all_users()
        self.assertEqual(all_users.status_code, 200)
