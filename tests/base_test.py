"""Hello Books Base Tests File"""

import run
from api import app, db
from config import app_config
from api.models import User

import unittest
from flask import json


class TestHelloBooks(unittest.TestCase):
    """Hello Books Test Base Class"""

    def setUp(self):
        """Set up function before any test runs"""
        self.app = app
        app.config.from_object(app_config['testing'])
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Registration Test Data
        self.user_data = {
            "email":"geof@yahoo.com",
            "username":"geof",
            "first_name":"Geof",
            "last_name":"Humphrey",
            "password":"password1234",
            "confirm_password":"password1234"
        }
        self.user_data2 = {
            "email":"hump@yahoo.com",
            "username":"geof",
            "first_name":"Geof",
            "last_name":"Humphrey",
            "password":"password1234",
            "confirm_password":"password1234"
        }
        self.empty_user_data = {

        }
        self.user_data_no_email = {
            "email":"",
            "username":"geof",
            "first_name":"Geof",
            "last_name":"Humphrey",
            "password":"password1234",
            "confirm_password":"password1234"
        }
        self.user_data_wrong_email = {
            "email":"hgtfd",
            "username":"geof",
            "first_name":"Geof",
            "last_name":"Humphrey",
            "password":"password1234",
            "confirm_password":"password1234"
        }
        self.user_data_long_email = {
            "email":"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn@gmail.com",
            "username":"geof",
            "first_name":"Geof",
            "last_name":"Humphrey",
            "password":"password1234",
            "confirm_password":"password1234"
        }
        self.user_data_no_username = {
            "email":"geof@yahoo.com",
            "username":"",
            "first_name":"Geof",
            "last_name":"Humphrey",
            "password":"password1234",
            "confirm_password":"password1234"
        }
        self.user_data_long_username = {
            "email":"geof@yahoo.com",
            "username":"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn",
            "first_name":"Geof",
            "last_name":"Humphrey",
            "password":"password1234",
            "confirm_password":"password1234"
        }
        self.user_data_no_first_name = {
            "email":"geof@yahoo.com",
            "username":"geof",
            "first_name":"",
            "last_name":"Humphrey",
            "password":"password1234",
            "confirm_password":"password1234"
        }
        self.user_data_long_first_name = {
            "email":"geof@yahoo.com",
            "username":"geof",
            "first_name":"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn",
            "last_name":"Humphrey",
            "password":"password1234",
            "confirm_password":"password1234"
        }
        self.user_data_no_last_name = {
            "email":"geof@yahoo.com",
            "username":"geof",
            "first_name":"Geof",
            "last_name":"",
            "password":"password1234",
            "confirm_password":"password1234"
        }
        self.user_data_long_last_name = {
            "email":"geof@yahoo.com",
            "username":"geof",
            "first_name":"Geof",
            "last_name":"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn",
            "password":"password1234",
            "confirm_password":"password1234"
        }
        self.user_data_no_password = {
            "email":"geof@yahoo.com",
            "username":"geof",
            "first_name":"Geof",
            "last_name":"Humphrey",
            "password":"",
            "confirm_password":""
        }
        self.user_data_short_password = {
            "email":"geof@yahoo.com",
            "username":"geof",
            "first_name":"Geof",
            "last_name":"Humphrey",
            "password":"pass",
            "confirm_password":"pass"
        }
        self.user_data_no_confirm = {
            "email":"geof@yahoo.com",
            "username":"geof",
            "first_name":"Geof",
            "last_name":"Humphrey",
            "password":"password1234",
            "confirm_password":""
        }
        self.user_data_password_mismatch = {
            "email":"geof@yahoo.com",
            "username":"geof",
            "first_name":"Geof",
            "last_name":"Humphrey",
            "password":"password1234",
            "confirm_password":"pass"
        }
        
        #Login Test Data
        self.login_data = {
            "username": "geof",
            "password": "password1234"
        }
        self.login_data_user_not_exist = {
            "username": "harry",
            "password": "password1234"
        }
        self.login_data_password_mismatch = {
            "username": "geof",
            "password": "password123"
        }
        self.book_data = {
            "title":"Windmills of Gods",
            "author":"Sidney Sheldon",
            "isbn":"36524728764",
            "publisher": "Publisher",
            "quantity": 45
        }
        self.empty_book_data = {

        }
        self.book_data_no_title = {
            "title":"",
            "author":"Sidney Sheldon",
            "isbn":"36524728764",
            "publisher": "Publisher",
            "quantity": 45
        }
        self.book_data_no_author = {
            "title":"Windmills of Gods",
            "author":"",
            "isbn":"36524728764",
            "publisher": "Publisher",
            "quantity": 45
        }
        self.book_data_no_isbn = {
            "title":"Windmills of Gods",
            "author":"Sidney Sheldon",
            "isbn":"",
            "publisher": "Publisher",
            "quantity": 45
        }
        self.book_data_no_publisher = {
            "title":"Windmills of Gods",
            "author":"Sidney Sheldon",
            "isbn":"36524728764",
            "publisher": "",
            "quantity": 45
        }
        self.book_data_no_quantity = {
            "title":"Windmills of Gods",
            "author":"Sidney Sheldon",
            "isbn":"36524728764",
            "publisher": "Publisher",
            "quantity": None
        }
        self.update_book_data = {
            "title":"Windmills of Gods",
            "author":"Sidney Sheldon",
            "isbn":"36524728764",
            "publisher": "Publisher",
            "quantity": 100
        }
        self.update_book_data_empty = {
          
        }
        self.update_book_data_no_title = {
            "title":"",
            "author":"Sidney Sheldon",
            "isbn":"36524728764",
            "publisher": "Publisher",
            "quantity": 100
        }
        self.update_book_data_no_author = {
            "title":"Windmills of Gods",
            "author":"",
            "isbn":"36524728764",
            "publisher": "Publisher",
            "quantity": 100
        }
        self.update_book_data_no_isbn = {
            "title":"Windmills of Gods",
            "author":"Sidney Sheldon",
            "isbn":"",
            "publisher": "Publisher",
            "quantity": 100
        }
        self.update_book_data_no_publisher = {
            "title":"Windmills of Gods",
            "author":"Sidney Sheldon",
            "isbn":"36524728764",
            "publisher": "",
            "quantity": 100
        }
        self.update_book_data_no_quantity = {
            "title":"Windmills of Gods",
            "author":"Sidney Sheldon",
            "isbn":"36524728764",
            "publisher": "Publisher",
            "quantity": None
        }
        admin = User('dmwangi@gmail.com', 'dmwangi', 'David', 'Mwangi', 'password1234')
        admin.is_admin = True
        admin.save()
        self.admin_data = {
            "username": "dmwangi",
            "password": "password1234",
        }

    def tearDown(self):
        """Tears down after every test runs"""
        db.session.close()
        db.drop_all()
        self.app_context.pop()

    def register_user(self, data):
        return self.client.post('/api/v1/auth/register', data=json.dumps(data), content_type='application/json')

    def login_user(self, data):
        return self.client.post('/api/v1/auth/login', data=json.dumps(data), content_type='application/json')

    def logout_user(self, user):
        msg = json.loads(user.data)
        print(msg)
        token = msg['Token']
        return self.client.post('/api/v1/auth/logout', headers={"Authorization": "Bearer {}".format(token)})

    def get_all_books(self):
        return self.client.get('/api/v1/books')

    def get_book(self, id):
        return self.client.get('/api/v1/book/' + str(id))

    def login_admin(self):
        return self.login_user(self.admin_data)

    def add_book(self, data):
        admin = self.login_admin()
        token = json.loads(admin.data)['Token']
        return self.client.post('/api/v1/books', data=json.dumps(data), headers={"Authorization": "Bearer {}".format(token)}, content_type='application/json')

    def update_book(self, data, id):
        admin = self.login_admin()
        token = json.loads(admin.data)['Token']
        return self.client.put('/api/v1/book/'+str(id), data=json.dumps(data), headers={"Authorization": "Bearer {}".format(token)}, content_type='application/json')

    def delete_book(self, id):
        admin = self.login_admin()
        token = json.loads(admin.data)['Token']
        return self.client.delete('/api/v1/book/'+str(id), headers={"Authorization": "Bearer {}".format(token)}, content_type='application/json')

    def get_all_users(self):
        admin = self.login_admin()
        token = json.loads(admin.data)['Token']
        return self.client.get('/api/v1/users', headers={"Authorization": "Bearer {}".format(token)}, content_type='application/json')
