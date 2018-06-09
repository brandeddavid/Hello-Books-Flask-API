"""
[
  init file
]
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask('__name__')

jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
app.config['JWT_BLACKLIST_ENABLED'] = False
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dmwangi:postgres@localhost/hellobooks_db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
