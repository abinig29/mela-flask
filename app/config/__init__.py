
from .development import DevelopmentConfig
from .production import ProductionConfig
from .cors import configure_cors


def configure_app(app):
    """Configure the Flask app with the appropriate settings."""
    environment = app.config.get("ENV", "development")

    if environment == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
    configure_cors(app)
