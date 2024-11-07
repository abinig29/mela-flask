# app/auth/routes.py
from flask import redirect, url_for
from flask_login import logout_user, login_required
from . import admin_auth


@admin_auth.route("/logout")
@login_required
def logout():
    print("logout")
    logout_user()
    return redirect(url_for("admin_auth.login"))
