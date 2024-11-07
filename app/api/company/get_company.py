from flask_restful import Resource
from app.model import Company
from app.schema.company import CompanySchema
from flask_jwt_extended import jwt_required, get_jwt_identity


class GetCompany(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()["id"]
        company = Company.query.filter_by(user_id=current_user_id).first()

        if not company:
            return {"message": "Company not found"}, 404

        schema = CompanySchema()
        return {"company": schema.dump(company)}, 200
