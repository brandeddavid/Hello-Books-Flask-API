"""
[
    File defines the user, book classes.
]
"""
from werkzeug.security import generate_password_hash, check_password_hash
from api import db

class User(db.Model):
    """
    [
        User Model
    ]
    """
    #Ensure table name is in plural
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        [
            Prevents password from being accessed
        ]
        """
        raise AttributeError("Password is not readable")

    @password.setter
    def password(self, password):
        """
        [
            Hashes user password
        ]
        Arguments:
            password {[str]} -- [User's password]
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        [
            Check is password hash matches actual password
        ]
        Arguments:
            password {[str]} -- [Password input]
        Returns:
            [bool] -- [True is matches, False is not]
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "User: {}".format(self.username)


class Book(db.Model):
    """
    [
        Book Model
    ]
    """
    #Ensure table name is in plural
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(68), index=True)
    author = db.Column(db.String(68), index=True)
    isbn = db.Column(db.String(68), index=True)
    publisher = db.Column(db.String(68), index=True)
    quantity = db.Column(db.Integer)
