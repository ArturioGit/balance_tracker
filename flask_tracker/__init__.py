from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    from flask_tracker.users.routes import users
    from flask_tracker.main.routes import main
    from flask_tracker.entries.routes import entries
    from flask_tracker.errors.handlers import errors
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    app.register_blueprint(errors)
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(entries)
    return app