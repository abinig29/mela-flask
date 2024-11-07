import os
from flask import send_from_directory, current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.model import Profile


class DownloadCV(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()["id"]

        profile = Profile.query.filter_by(user_id=current_user_id).first()
        if not profile or not profile.cv_link:
            return {"message": "CV not found."}, 404  # Not Found

        # Extract the filename from cv_link
        filename = os.path.basename(profile.cv_link)
        upload_folder = os.path.join(current_app.root_path, "uploads/cvs")

        # Serve the file
        return send_from_directory(
            directory=upload_folder,
            path=filename,
            as_attachment=True,  # Download as an attachment
        )
