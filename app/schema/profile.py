from flask_restful import fields


profile_fields = {
    "id": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "date_of_birth": fields.String,
    "phone_number": fields.String,
    "address_line_1": fields.String,
    "city": fields.String,
    "state": fields.String,
    "country": fields.String,
    "website": fields.String,
    "linkedin_profile": fields.String,
    "github_profile": fields.String,
    "cv_link": fields.String,
    "education": fields.List(fields.Raw),  # List of education details
    "experience": fields.List(fields.Raw),  # List of experience details
    "preferences": fields.Nested(
        {
            "preferred_location": fields.String,
            "full_time": fields.Boolean,
            "part_time": fields.Boolean,
            "remote": fields.Boolean,
            "skills": fields.List(fields.String),  # List of skill names
            "categories": fields.List(fields.String),  # List of category names
        }
    ),
}

user_fields = {
    "email": fields.String,
    "username": fields.String,
    "profile": fields.Nested(profile_fields),
}
