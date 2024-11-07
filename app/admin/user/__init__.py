from flask import Blueprint

admin_user = Blueprint("admin_user", __name__)
from .get_user import *
from .get_single_delete import *
