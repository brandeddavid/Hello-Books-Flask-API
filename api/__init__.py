from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask('__name__')

app.config['JWT_SECRET_KEY'] = 'super-secret-key'
app.config['JWT_BLACKLIST_ENABLED'] = False
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/hello_books'

db = SQLAlchemy(app)
blacklist = set()

users = {}
books = {}