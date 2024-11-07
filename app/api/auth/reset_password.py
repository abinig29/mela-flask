import time
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from app.extension import db
from app.model import User
from app.schema import auth
from app.service.otp_service import reset_password


class ResetPassword(Resource):
    def post(self):
        schema = auth.ResetPasswordSchema()
        try:

            data = schema.load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        email = data["email"]
        otp = data["otp"]
        new_password = data["new_password"]

        response, status_code = reset_password(email, otp, new_password)

        return response, status_code
