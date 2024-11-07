from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from app import db
from app.model import Company
from app.schema.company import CompanySchema
from flask_jwt_extended import jwt_required, get_jwt_identity


class EditCompany(Resource):
    @jwt_required()
    def put(self):
        current_user_id = get_jwt_identity()["id"]
        company = Company.query.filter_by(user_id=current_user_id).first()
        if not company:
            return {"message": "Company not found"}, 404

        schema = CompanySchema(partial=True)
        try:
            data = schema.load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        company.name = data.get("name", company.name)
        company.email = data.get("email", company.email)
        company.website = data.get("website", company.website)
        company.location = data.get("location", company.location)

        db.session.commit()

        return {"company": schema.dump(company)}, 200
