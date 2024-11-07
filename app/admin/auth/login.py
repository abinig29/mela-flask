# app/auth/routes.py
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import admin_auth
from app.model import User, RoleType
from app.forms import LoginForm


@admin_auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = User.query.filter_by(email=form.email.data, role=RoleType.ADMIN).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            return redirect(url_for("admin_dashboard.dashboard"))
        else:
            flash("Invalid email or password", category="danger")
    return render_template("login.html", form=form)
