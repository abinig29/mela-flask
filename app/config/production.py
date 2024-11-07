from .config import Config
import os
from dotenv import load_dotenv
load_dotenv()

class ProductionConfig(Config):
    """Production-specific configuration."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///prod.db")
    FLASK_ENV = "production"
    CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]
    CORS_METHODS = ["GET", "POST", "PUT", "DELETE"]
    CORS_HEADERS = ["Content-Type", "Authorization"]

    # Production-specific settings (e.g., stricter security, logging)
    # PROPAGATE_EXCEPTIONS = True
