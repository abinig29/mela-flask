from .config import Config
import os
from dotenv import load_dotenv
load_dotenv()

class DevelopmentConfig(Config):
    """Development-specific configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URI", "sqlite:///dev.db")
    FLASK_ENV = "development"
    CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]
    CORS_METHODS = ["GET", "POST", "PUT", "DELETE"]
    CORS_HEADERS = ["Content-Type", "Authorization"]
    # Other dev-specific configs can go here
