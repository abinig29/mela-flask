import random
import time
from flask import request
from flask_restful import Resource
from flask_mail import Message
from app.extension import db, mail
from app.model import User
from marshmallow import ValidationError
from app.schema import auth


class ForgotPassword(Resource):
    def post(self):
        schema = auth.PasswordResetRequestSchema()
        try:
            data = schema.load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        # Check if user exists
        user = User.query.filter_by(email=data["email"]).first()
        if user is None:
            return {"message": "Email not found."}, 404

        otp = str(random.randint(100000, 999999))
        user.set_verification_code(otp)
        user.verification_code_expires = int(time.time()) + 600
        db.session.commit()

        # Send OTP via email
        msg = Message("Your OTP Code", recipients=[user.email])
        msg.body = f"Your OTP code is {otp}. It will expire in 10 minutes."
        mail.send(msg)

        return {"message": "OTP sent to your email."}, 200
