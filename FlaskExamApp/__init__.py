from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from FlaskExamApp.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from FlaskExamApp.users.Routes import users
    from FlaskExamApp.exams.Routes import exams
    from FlaskExamApp.main.Routes import main

    app.register_blueprint(users)
    app.register_blueprint(exams)
    app.register_blueprint(main)

    return app