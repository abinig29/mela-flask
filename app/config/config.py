import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration with default settings."""

    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_jwt_secret_key")
    CORS_HEADERS = "Content-Type"
    # Configure Flask-Mail
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT", 587)
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", True)
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
