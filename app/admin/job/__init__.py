from flask import Blueprint

admin_job = Blueprint("admin_job", __name__)
from .get_job import *
