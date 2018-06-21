from api import db, app
from api import routes
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

app.register_blueprint(routes.mod)


manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
