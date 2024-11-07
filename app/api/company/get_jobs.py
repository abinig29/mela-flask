from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.model import Job, Company


class GetCompanyJobs(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()["id"]
        company = Company.query.filter_by(user_id=current_user_id).first()
        if not company:
            return {"message": "Company not found"}, 404
        jobs = Job.query.filter_by(company_id=company.id).all()
        return {"jobs": [job.to_dict() for job in jobs]}, 200
