from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from marshmallow import ValidationError
from app.model import User
from app.schema import auth
from datetime import timedelta


class Login(Resource):
    def post(self):
        schema = auth.UserLoginSchema()
        try:
            data = schema.load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        user = User.query.filter(User.email == data["email"]).first()

        if user is None:
            return {"message": "Invalid username or password."}, 401

        if not user.check_password(data["password"]):
            return {"message": "Invalid username or password."}, 401

        access_token = create_access_token(
            identity={"id": user.id, "role": user.role.name},
            expires_delta=timedelta(days=7),
        )
        return {"access_token": access_token}, 200
