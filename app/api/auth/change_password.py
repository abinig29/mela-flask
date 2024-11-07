from flask import request
from flask_restful import Resource
from marshmallow import Schema, fields, ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extension import db
from app.model import User
from app.schema.auth import ChangePasswordSchema


class ChangePassword(Resource):
    @jwt_required()
    def patch(self):
        schema = ChangePasswordSchema()
        try:
            data = schema.load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        signed_user = get_jwt_identity()
        user = User.query.get(signed_user["id"])

        if user is None:
            return {"message": "User not found."}, 404

        if not user.check_password(data["current_password"]):
            return {"message": "Current password is incorrect."}, 400

        user.set_password(data["new_password"])
        db.session.commit()

        return {"message": "Password changed successfully."}, 200
