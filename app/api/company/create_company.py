from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from app import db
from app.model import Company
from app.schema.company import (
    CompanySchema,
)  # Import your Company schema for validation
from flask_jwt_extended import jwt_required, get_jwt_identity


class CreateCompany(Resource):
    @jwt_required()
    def post(self):
        schema = CompanySchema()
        try:
            data = schema.load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        if Company.query.filter(
            (Company.email == data.get("email"))
            | (Company.website == data.get("website"))
        ).first():
            return {
                "message": "A company with this email or website already exists."
            }, 400
        current_user_id = get_jwt_identity()["id"]
        company = Company(
            user_id=current_user_id,
            name=data["name"],
            email=data.get("email", ""),
            website=data.get("website", ""),
            location=data.get("location", ""),
        )

        db.session.add(company)
        db.session.commit()

        return {"company": schema.dump(company)}, 201
