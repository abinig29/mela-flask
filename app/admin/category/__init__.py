from flask import Blueprint

admin_category = Blueprint("admin_category", __name__)
from .get_post_category import *
from .delete_category import *
