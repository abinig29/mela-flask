from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from app import db
from app.model import Company, Job, Skill, Category
from app.schema.job import JobSchema
from flask_jwt_extended import jwt_required, get_jwt_identity


class PostJob(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()["id"]
        company = Company.query.filter_by(user_id=current_user_id).first()
        if not company:
            return {"message": "Company not found"}, 404

        schema = JobSchema()
        try:
            data = schema.load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400
        job = Job(
            title=data["title"],
            description=data["description"],
            company_name=company.name,
            location=data.get("location", ""),
            application_link=data.get("application_link", ""),
            company_id=company.id,
            source="Company",
            job_type=data.get("job_type"),
            experience_level=data.get("experience_level"),
        )

        skills = data.get("skill_ids", [])
        for skill_id in skills:
            skill = Skill.query.get(skill_id)
            if skill:
                job.skills.append(skill)

        category_ids = data.get("category_ids", [])
        for category_id in category_ids:
            category = Category.query.get(category_id)
            if category:
                job.categories.append(category)

        db.session.add(job)
        db.session.commit()

        return {"job": schema.dump(job)}, 201
