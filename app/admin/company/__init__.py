from flask import Blueprint

admin_company = Blueprint("admin_company", __name__)

from .get_single_delete import *
from .get_company import *
