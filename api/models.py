"""
[
    File defines the user, book classes.
]
"""
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
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
    borrowed_books = db.relationship('Book', secondary='borrowed_books', lazy='dynamic')

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

    @staticmethod
    def get_user_by_username(username):
        """[summary]
        
        Arguments:
            username {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        return User.query.filter_by(username=username).first()
    
    def update_password(self, password):
        """[summary]
        
        Arguments:
            password {[type]} -- [description]
        """
        self.hash_password = User.hash_password(password)
        User.save(self)
    
    @property
    def serialize(self):
        """[summary]
        
        Returns:
            [type] -- [description]
        """
        return {
            "email": self.email,
            "username": self.username,
            "full_name": self.first_name + " " + self.last_name,
            "is_admin": self.is_admin,
        }

    @property  
    def promote(self):
        """[summary]
        """
        if self.is_admin == True:
            pass
        self.is_admin = True
        User.save(self)

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
    borrowers = db.relationship('User', secondary='borrowed_books', lazy='dynamic')

    def __init__(self, title, author, isbn, publisher, quantity):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publisher = publisher
        self.quantity = quantity

    @staticmethod
    def get_all_books():
        """[summary]
        
        Returns:
            [type] -- [description]
        """
        return Book.query.all()

    @staticmethod
    def get_book_by_id(id):
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

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "Book: {}".format(self.title)


class BorrowBook(db.Model):
    """
    [
        Association Table
    ]
    
    Arguments:
        db {[type]} -- [description]
    """
    __tablename__="borrowed_books"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    date_borrowed = db.Column(db.DateTime, default=datetime.now())
    date_due = db.Column(db.DateTime, default=datetime.now()+timedelta(days=30))
    returned = db.Column(db.Boolean, default=False)
    date_returned = db.Column(db.DateTime, nullable=True)
    user = db.relationship(User, backref='book')
    book = db.relationship(Book, backref='user')

    @staticmethod
    def get_all_borrowed_books():
        """[summary]
        
        Returns:
            [type] -- [description]
        """
        return BorrowBook.query.all()

    @staticmethod
    def get_user_borrowing_history(user_id):
        """[summary]
        
        Arguments:
            user_id {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        borrowed_books = BorrowBook.get_all_borrowed_books()
        user_books = [book for book in borrowed_books if book.user_id == user_id]
        borrowing_history = []
        book_details = {}
        for book in user_books:
            book_details["Title"] = Book.get_book_by_id(book.book_id).title
            book_details["Date Borrowed"] = book.date_borrowed
            if book.returned:
                book_details["Date Returned"] = book.date_returned
            else:
                book_details["Due Date"] = book.date_due
            borrowing_history.append(book_details)
        return borrowing_history

    @staticmethod
    def get_books_not_returned(user_id):
        """[summary]
        
        Arguments:
            user_id {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        borrowed_books = BorrowBook.get_all_borrowed_books()
        # User non returned books
        user_books = [book for book in borrowed_books if book.user_id == user_id and book.returned == False]
        unreturned_books = []
        book_details = {}
        for book in user_books:
            book_details["Title"] = Book.get_book_by_id(book.book_id).title
            book_details["Date Borrowed"] = book.date_borrowed
            book_details["Due Date"] = book.date_due
            unreturned_books.append(book_details)
        return unreturned_books

    def save(self):
        """
        [summary]
        """
        db.session.add(self)
        db.session.commit()

class Token(db.Model):
    """[summary]
    
    Arguments:
        db {[type]} -- [description]
    """
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(1000), index=True, unique=True)
    owner = db.Column(db.String(60))
    created = db.Column(db.DateTime, default=datetime.today())

    def __init__(self, token, owner):
        self.token = token
        self.owner = owner

    @staticmethod
    def all_tokens():
        return Token.query.all()

    @staticmethod
    def token_by_owner(username):
        return Token.query.filter_by(owner=username).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Revoked(db.Model):
    """[summary]
    
    Arguments:
        db {[type]} -- [description]
    """

    __tablename__ = 'revoked'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(1000), index=True)
    date_revoked = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, token):
        self.token = token

    @staticmethod
    def is_blacklisted(token):
        if Revoked.query.filter_by(token=token).first():
            return True
        return False

    def save(self):
        db.session.add(self)
        db.session.commit()

