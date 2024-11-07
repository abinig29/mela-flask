from flask_restful import Resource, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schema.profile import user_fields
from app.model import User, Profile, Experience, Education, UserPreferences


class GetProfile(Resource):
    @jwt_required()
    @marshal_with(user_fields)
    def get(self):
        current_user_id = get_jwt_identity()["id"]

        # Fetch user details
        user = User.query.get(current_user_id)
        if not user:
            return {"message": "User not found."}, 404

        # Fetch the profile associated with the user
        profile = Profile.query.filter_by(user_id=current_user_id).first()
        if not profile:
            return {"message": "Profile not found."}, 404

        print(profile.cv_link, "cv link")

        # Fetch related education, experience, and preferences
        education = Education.query.filter_by(profile_id=profile.id).all()
        experiences = Experience.query.filter_by(profile_id=profile.id).all()
        preferences = UserPreferences.query.filter_by(profile_id=profile.id).first()

        # Prepare response
        response = {
            "email": user.email,
            "username": user.username,
            "profile": {
                "id": str(profile.id),
                "first_name": profile.first_name,
                "last_name": profile.last_name,
                "date_of_birth": (
                    profile.date_of_birth.isoformat() if profile.date_of_birth else None
                ),
                "phone_number": profile.phone_number,
                "address_line_1": profile.address_line_1,
                "city": profile.city,
                "state": profile.state,
                "country": profile.country,
                "website": profile.website,
                "linkedin_profile": profile.linkedin_profile,
                "github_profile": profile.github_profile,
                "cv_link": profile.cv_link,
                "education": [
                    {
                        "id": str(edu.id),
                        "institution": edu.institution,
                        "degree": edu.degree,
                        "field_of_study": edu.field_of_study,
                        "from_year": edu.from_year,
                        "to_year": edu.to_year,
                    }
                    for edu in education
                ],
                "experience": [
                    {
                        "id": str(exp.id),
                        "company": exp.company,
                        "role": exp.role,
                        "from_date": (
                            exp.from_date.isoformat() if exp.from_date else None
                        ),
                        "to_date": exp.to_date.isoformat() if exp.to_date else None,  #
                        "remarks": exp.remarks,
                    }
                    for exp in experiences
                ],
                "preferences": {
                    "preferred_location": (
                        preferences.preferred_location if preferences else None
                    ),
                    "full_time": preferences.full_time if preferences else False,
                    "part_time": preferences.part_time if preferences else False,
                    "remote": preferences.remote if preferences else False,
                    "skills": (
                        [skill.skill_name for skill in preferences.skills]
                        if preferences
                        else []
                    ),
                    "categories": (
                        [category.name for category in preferences.categories]
                        if preferences
                        else []
                    ),
                },
            },
        }

        return response, 200
