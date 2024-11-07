# config/cors.py

from flask_cors import CORS


def configure_cors(app):
    CORS(
        app,
        resources={
            r"/*": {
                "origins": app.config["CORS_ORIGINS"],
                "methods": app.config["CORS_METHODS"],
                "allow_headers": app.config["CORS_HEADERS"],
                "supports_credentials": True,
            }
        },
    )
