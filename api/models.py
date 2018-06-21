"""
[
    File defines the user, book classes and the association object.
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
        """
        [
            Init function
        ]
        
        Arguments:
            email {[str]} -- [User's email]
            username {[str]} -- [User's username]
            first_name {[str]} -- [User's first_name]
            last_name {[str]} -- [User's last_name]
            password {[str]} -- [User's password]
        """
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
            Saves user objects to database
        ]
        """
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def all_users():
        """
        [
            Gets all users
        ]
        
        Returns:
            [list] -- [List of all user objects]
        """
        return User.query.all()

    @staticmethod
    def get_user_by_username(username):
        """
        [
            Gets user by username
        ]
        
        Arguments:
            username {[str]} -- [User's username]
        
        Returns:
            [object] -- [User object]
        """
        return User.query.filter_by(username=username).first()
    
    def update_password(self, password):
        """
        [
            Updates user's password
        ]
        
        Arguments:
            password {[str]} -- [User's new password]
        """
        self.hash_password = User.hash_password(password)
        User.save(self)
    
    @property
    def serialize(self):
        """
        [
            Serializes User object
        ]
        
        Returns:
            [dict] -- [Dict with user info]
        """
        return {
            "email": self.email,
            "username": self.username,
            "full_name": self.first_name + " " + self.last_name,
            "is_admin": self.is_admin,
        }

    @property  
    def promote(self):
        """
        [
            Promotes normal user to admin
        ]
        """
        if self.is_admin == True:
            pass
        self.is_admin = True
        User.save(self)

    @staticmethod
    def promote_user(username):
        """
        [
            Promotes normal user to admin in tests
        ]
        """
        user = User.get_user_by_username(username)
        user.is_admin = True
        user.save()

    def admin(self):
        """
        [
            Checks if user is an admin
        ]
        
        Returns:
            [boolean] -- [True if user is admin and false if not]
        """
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
        """
        [
            Init function
        ]
        
        Arguments:
            title {[str]} -- [Book's title]
            author {[str]} -- [Book's author]
            isbn {str} -- [Book's isbn]
            publisher {[str]} -- [Book's publisher]
            quantity {[str]} -- [Copies of book]
        """
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publisher = publisher
        self.quantity = quantity

    @staticmethod
    def get_all_books():
        """
        [
            Gets all book
        ]
        
        Returns:
            [list] -- [list of book objects]
        """
        return Book.query.all()

    @staticmethod
    def get_book_by_id(id):
        """
        [
            Gets book by id
        ]
        
        Arguments:
            id {[str]} -- [Book's id]
        
        Returns:
            [object] -- [Book object]
        """
        return Book.query.filter_by(id=id).first()
    
    @property
    def serialize(self):
        """
        [
            Serializes book information
        ]
        
        Returns:
            [Dict] -- [Dict object with book information]
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
        """
        [
            Saves book object to database
        ]
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        [
            Deletes book object
        ]
        """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "Book: {}".format(self.title)


class BorrowBook(db.Model):
    """
    [
        Association Table
    ]
    """
    __tablename__="borrowed_books"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    date_borrowed = db.Column(db.Date, default=datetime.today())
    date_due = db.Column(db.Date, default=datetime.today()+timedelta(days=30))
    returned = db.Column(db.Boolean, default=False)
    date_returned = db.Column(db.Date, nullable=True)
    user = db.relationship(User, backref='book')
    book = db.relationship(Book, backref='user')

    @staticmethod
    def get_all_borrowed_books():
        """
        [
            Gets all books in borrow table
        ]
        
        Returns:
            [list] -- [list of book objects in borrow table]
        """
        return BorrowBook.query.all()

    @staticmethod
    def get_user_borrowing_history(user_id):
        """
        [
            Gets user borrowing history
        ]
        
        Arguments:
            user_id {[str]} -- [user id]
        
        Returns:
            [list] -- [List of books borrowed by user]
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
        """
        [
            Gets books not returned by user
        ]
        
        Arguments:
            user_id {[str]} -- [user is]
        
        Returns:
            [list] -- [books not returned by user]
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
        [
            Saved book borrowed to database
        ]
        """
        db.session.add(self)
        db.session.commit()

class Token(db.Model):
    """
    [
        Token Model
    ]
    """
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(1000), index=True, unique=True)
    owner = db.Column(db.String(60))
    created = db.Column(db.DateTime, default=datetime.today())

    def __init__(self, token, owner):
        """
        [
            Init function
        ]
        
        Arguments:
            token {[str]} -- [User token]
            owner {[str]} -- [Token owner]
        """
        self.token = token
        self.owner = owner

    @staticmethod
    def all_tokens():
        """
        [
            Gets all tokens
        ]
        
        Returns:
            [list] -- [list of all tokens]
        """
        return Token.query.all()

    @staticmethod
    def token_by_owner(username):
        """
        [
            Gets token by user's username
        ]
        
        Arguments:
            username {[str]} -- [user's username]
        
        Returns:
            [object] -- [Token object]
        """
        return Token.query.filter_by(owner=username).first()

    def save(self):
        """
        [
            Saves generated token to database.
        ]
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        [
            Delete token after being revoked
        ]
        """
        db.session.delete(self)
        db.session.commit()

class Revoked(db.Model):
    """
    [
        Revoked Token Table
    ]
    """

    __tablename__ = 'revoked'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(1000), index=True)
    date_revoked = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, token):
        """
        [
            Init function
        ]
        
        Arguments:
            token {[str]} -- [User token]
        """
        self.token = token

    @staticmethod
    def is_blacklisted(token):
        """
        [
            Checks if token is revoked
        ]
        
        Arguments:
            token {[str]} -- [User token]
        
        Returns:
            [boolean] -- [True if revoked, false if not]
        """
        if Revoked.query.filter_by(token=token).first():
            return True
        return False

    def save(self):
        """
        [
            Saves revoked token to database
        ]
        """
        db.session.add(self)
        db.session.commit()

