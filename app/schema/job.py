from marshmallow import Schema, fields, validates, ValidationError, validate
from app.model.job import Category, JobType, ExperienceLevel
from app.model.profile.skill import Skill


class JobSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    location = fields.String(required=False, allow_none=True)
    application_link = fields.String(required=False, allow_none=True)
    source = fields.String(required=False, allow_none=True)

    skill_ids = fields.List(fields.String(), required=False, allow_none=True)
    category_ids = fields.List(fields.UUID(), required=False, allow_none=True)

    job_type = fields.Str(
        required=False,
        validate=validate.OneOf([job_type.name for job_type in JobType]),
    )
    experience_level = fields.Str(
        required=False,
        validate=validate.OneOf([level.name for level in ExperienceLevel]),
    )

    @validates("category_ids")
    def validate_category_ids(self, value):
        """Validate that each category_id exists in the database."""
        for category_id in value:
            if not Category.query.get(category_id):
                raise ValidationError(f"Category with ID {category_id} does not exist.")

    @validates("skill_ids")
    def validate_skill_ids(self, value):
        """Validate that each skill_id exists in the database."""
        for skill_id in value:
            if not Skill.query.get(skill_id):
                raise ValidationError(f"Skill with ID {skill_id} does not exist.")

    class Meta:
        ordered = True
