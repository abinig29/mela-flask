import time
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from app.extension import db
from app.model import User
from app.schema import auth


class VerifyOTP(Resource):
    def post(self):
        schema = auth.OTPVerificationSchema()
        try:
            data = schema.load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        # Find the user by email
        user = User.query.filter_by(email=data["email"]).first()
        if user is None:
            return {"message": "Email not found."}, 404

        # Check if verification_code_expires is set
        if user.verification_code_expires is None:
            return {"message": "OTP verification has not been initiated."}, 400

        # Check if the OTP is valid and not expired
        if user.verification_code_expires < int(time.time()):
            return {"message": "OTP has expired."}, 400

        if not user.check_verification_code(data["otp"]):
            return {"message": "Invalid OTP."}, 400

        # Reset verification fields upon successful verification
        user.verification_code_hash = None
        user.verification_code_expires = None
        db.session.commit()

        return {
            "message": "OTP verified successfully. You can now reset your password."
        }, 200
