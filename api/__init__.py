from flask import Flask

app = Flask('__name__')

app.config['JWT_SECRET_KEY'] = 'super-secret-key'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']


users = []
books = []