from .auth import auth_bp
from .profile import profile_bp
from .upload import upload_bp
from .company import company_bp


def configure_blueprint(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(profile_bp, url_prefix="/api/profile")
    app.register_blueprint(upload_bp, url_prefix="/api/upload")
    app.register_blueprint(company_bp, url_prefix="/api/company")
