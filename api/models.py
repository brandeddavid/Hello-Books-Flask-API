"""
[
    File defines the user, book classes.
]
"""
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
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
    joined = db.Column(db.Date, default=datetime.today())

    def __init__(self, email, username, first_name, last_name, password):
        self.email = email
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = self.hash_password(password)

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

    @staticmethod
    def verify_password(saved_password, password):
        """
        [
            Check is password hash matches actual password
        ]
        Arguments:
            password {[str]} -- [Password input]
        Returns:
            [bool] -- [True is matches, False is not]
        """
        return check_password_hash(saved_password, password)
    
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
    
    def admin(self):
        if self.is_admin:
            return True
        return False

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
    title = db.Column(db.String(500), index=True)
    author = db.Column(db.String(100), index=True)
    isbn = db.Column(db.String(100), index=True, unique=True)
    publisher = db.Column(db.String(100), index=True)
    quantity = db.Column(db.Integer)
    availability = False
    created = db.Column(db.Date, default=datetime.today())

    def __init__(self, title, author, isbn, publisher, quantity):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publisher = publisher
        self.quantity = quantity

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
        else:
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


class Token(db.Model):
    """[summary]
    
    Arguments:
        db {[type]} -- [description]
    """
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, default=datetime.today())

    def __init__(self, token, owner):
        self.token = token
        self.owner = owner

    def save(self):
        db.session.add(self)
        db.session.commit()


# admin = User('david.mathenge98@gmail.com', 'dmwangi', 'David', 'Mwangi', 'marigi@98').save()
# admin.is_admin = True