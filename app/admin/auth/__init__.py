from flask import Blueprint

admin_auth = Blueprint("admin_auth", __name__)
from .login import *
from .logout import *
