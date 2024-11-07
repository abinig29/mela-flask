# app/forms.py
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class CategoryForm(FlaskForm):
    name = StringField("Category Name", validators=[DataRequired()])
    submit = SubmitField("Add Category")
