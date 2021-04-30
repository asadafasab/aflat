from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import concurrent.futures

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "TODO secret key here"  # TODO
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from aflat.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from aflat.auth import auth as auth_

    app.register_blueprint(auth_)

    from aflat.noauth import noauth as noauth_

    app.register_blueprint(noauth_)

    return app


db.create_all(app=create_app())
