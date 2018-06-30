"""Manage file"""

from api import db, app
from api import routes
from api.models import User
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

app.register_blueprint(routes.mod)


manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def create_admin():
    """Create admin function"""
    email = input('Enter email: ')
    username = input('Enter username: ')
    first_name = input('Enter first name: ')
    last_name = input('Enter last name: ')
    password = input('Enter password: ')
    try:
        admin = User(email, username, first_name, last_name, password)
        admin.is_admin = True
        admin.save()
    except Exception as e:
        print(e)
    print('Admin user created successfully')

if __name__ == '__main__':
    manager.run()
