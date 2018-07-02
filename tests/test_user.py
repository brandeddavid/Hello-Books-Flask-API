from tests.base_test import TestHelloBooks
import json

class UserTestCase(TestHelloBooks):

    def test_get_users(self):
        self.register_user(self.user_data)
        all_users = self.get_all_users()
        self.assertEqual(all_users.status_code, 200)
