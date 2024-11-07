from flask import request
from flask_restful import Resource, Api
from marshmallow import ValidationError
from app.model import User, RoleType, AccountStatus, AuthProvider
from app.schema import auth
from app.extension import db


class Register(Resource):
    def post(self):
        schema = auth.UserRegisterSchema()
        try:
            data = schema.load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        existing_user = User.query.filter(
            (User.username == data["username"]) | (User.email == data["email"])
        ).first()

        if existing_user:
            return {"message": "User with this username or email already exists."}, 409

        new_user = User(
            email=data["email"],
            username=data["username"],
            first_time_login=True,
        )

        new_user = User(
            email=data["email"],
            username=data["username"],
            first_time_login=True,
            role=RoleType.USER,
            account_status=AccountStatus.VERIFIED,
            active=True,
            auth_provider=AuthProvider.CREDENTIAL,
        )

        new_user.set_password(data["password"])

        db.session.add(new_user)
        db.session.commit()

        return {"message": "User registered successfully."}, 201
