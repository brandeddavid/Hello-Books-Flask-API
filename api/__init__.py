from flask import Flask

app = Flask('__name__')

app.config['JWT_SECRET_KEY'] = 'super-secret-key'