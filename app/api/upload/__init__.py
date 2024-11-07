from flask import Blueprint
from flask_restful import Api
from .cv_upload import UploadCV
from .get_cv import DownloadCV


upload_bp = Blueprint("upload", __name__)
api = Api(upload_bp)

api.add_resource(UploadCV, "/cv")
api.add_resource(DownloadCV, "/download_cV")
