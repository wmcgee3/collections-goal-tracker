from flask import Flask, session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from goal_tracker.config import Config

bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from goal_tracker.auth.routes import auth
        from goal_tracker.main.routes import main
        from goal_tracker.record.routes import record

        app.register_blueprint(auth)
        app.register_blueprint(main)
        app.register_blueprint(record)

        return app
