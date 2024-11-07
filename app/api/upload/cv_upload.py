import os
from flask import request, current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app.extension import db
from app.model import Profile
from app.config.upload import allowed_file, UPLOAD_FOLDER, MAX_CV_SIZE


class UploadCV(Resource):
    @jwt_required()
    def post(self):
        if "cv" not in request.files:
            return {"message": "No CV file provided."}, 400
        cv_file = request.files["cv"]
        if not allowed_file(cv_file.filename):
            return {
                "message": "File type not allowed. Allowed types: pdf, doc, docx."
            }, 400  # Bad Request

        if cv_file.content_length > MAX_CV_SIZE:
            return {"message": "File size exceeds 5 MB."}, 400

        current_user_id = get_jwt_identity()["id"]

        profile = Profile.query.filter_by(user_id=current_user_id).first()
        if not profile:
            return {"message": "Profile not found."}, 404  # Not Found

        filename = secure_filename(cv_file.filename)

        # Define upload folder and ensure it exists
        upload_folder = os.path.join(current_app.root_path, UPLOAD_FOLDER, "cvs")
        os.makedirs(upload_folder, exist_ok=True)

        # Save the file
        cv_path = os.path.join(upload_folder, filename)
        cv_file.save(cv_path)

        # Save the CV link in the profile
        profile.cv_link = f"/{UPLOAD_FOLDER}cvs/{filename}"

        # Commit the changes to the database
        db.session.commit()

        return {
            "cv_link": profile.cv_link,
        }, 201
