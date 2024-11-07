from flask import Flask, send_from_directory
import os

from app.extension import db, migrate, bcrypt, jwt, mail
from app.config import configure_app
from app.model import *
from app.model.user import User
from flask_jwt_extended import jwt_required
from .extension import login_manager


def create_app():
    app = Flask(__name__, template_folder="templates")

    configure_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "admin_auth.login"

    from app.api import configure_blueprint
    from app.admin import configure_admin_blueprint

    configure_blueprint(app)
    configure_admin_blueprint(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
