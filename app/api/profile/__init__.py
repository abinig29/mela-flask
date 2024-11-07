from flask import Blueprint
from flask_restful import Api
from .create_profile import CreateProfile
from .get_profile import GetProfile
from .update_profile import UpdateProfile


profile_bp = Blueprint("profile", __name__)
api = Api(profile_bp)

api.add_resource(CreateProfile, "/")
api.add_resource(GetProfile, "/")
api.add_resource(UpdateProfile, "/")
