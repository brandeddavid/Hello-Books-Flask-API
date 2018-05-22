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

    def __init__(self, email, username, first_name, last_name, password):
        self.email = email
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = self.hash_password(password)

    # @property
    # def password(self):
    #     """
    #     [
    #         Prevents password from being accessed
    #     ]
    #     """
    #     raise AttributeError("Password is not readable")

    @staticmethod
    def hash_password(password):
        """
        [
            Hashes user password
        ]
        Arguments:
            password {[str]} -- [User's password]
        """
        return generate_password_hash(password)

    def verify_password(password):
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
    
    def save(self):
        """
        [
            
        ]
        """
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def all_users():
        """[summary]
        
        Returns:
            [type] -- [description]
        """

        return User.query.all()
    
    @property
    def serialize(self):
        return {
            "email": self.email,
            "username": self.username,
            "full_name": self.first_name + " " + self.last_name,
            "is_admin": self.is_admin,
        }

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
    quantity = db.Column(db.Integer, default=0)
    availability = False

    @staticmethod
    def all_books():
        """[summary]
        
        Returns:
            [type] -- [description]
        """
        return Book.query.all()

    @staticmethod
    def book_by_id(id):
        """[summary]
        
        Arguments:
            id {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        return Book.query.filter_by(id=id).first()
    
    @property
    def serialize(self):
        """[summary]
        
        Returns:
            [type] -- [description]
        """
        if self.quantity == 0:
            self.availability = False
        self.availability = True
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "publisher": self.publisher,
            "availability": self.availability
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "Book: {}".format(self.title)
