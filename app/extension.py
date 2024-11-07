from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_login import LoginManager

migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
