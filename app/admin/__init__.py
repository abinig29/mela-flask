from .auth import admin_auth
from .dashboard import dashboard_bp
from .user import admin_user
from .job import admin_job
from .category import admin_category
from .company import admin_company


def configure_admin_blueprint(app):
    app.register_blueprint(admin_auth, url_prefix="/admin/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/admin/dashboard")
    app.register_blueprint(admin_user, url_prefix="/admin/user")
    app.register_blueprint(admin_job, url_prefix="/admin/job")
    app.register_blueprint(admin_category, url_prefix="/admin/category")
    app.register_blueprint(admin_company, url_prefix="/admin/company")
