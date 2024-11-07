from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extension import db
from app.model import Profile, Experience, Education, UserPreferences


class UpdateProfile(Resource):
    @jwt_required()
    def patch(self):
        current_user_id = get_jwt_identity()["id"]
        data = request.json

        profile = Profile.query.filter_by(user_id=current_user_id).first()
        if not profile:
            return {"message": "Profile not found."}, 404  # Not Found

        # Update profile details
        profile.first_name = data.get("first_name", profile.first_name)
        profile.last_name = data.get("last_name", profile.last_name)
        profile.date_of_birth = data.get("date_of_birth", profile.date_of_birth)
        profile.phone_number = data.get("phone_number", profile.phone_number)
        profile.address_line_1 = data.get("address_line_1", profile.address_line_1)
        profile.city = data.get("city", profile.city)
        profile.state = data.get("state", profile.state)
        profile.country = data.get("country", profile.country)
        profile.website = data.get("website", profile.website)
        profile.linkedin_profile = data.get(
            "linkedin_profile", profile.linkedin_profile
        )
        profile.github_profile = data.get("github_profile", profile.github_profile)

        # Update experiences if provided
        experiences_data = data.get("experiences", [])
        db.session.query(Experience).filter_by(profile_id=profile.id).delete()

        for exp in experiences_data:
            experience = Experience(
                profile_id=profile.id,
                company=exp.get("company"),
                role=exp.get("role"),
                from_date=exp.get("from_date"),
                to_date=exp.get("to_date"),
                remarks=exp.get("remarks"),
            )
            db.session.add(experience)

        educations_data = data.get("educations", [])
        db.session.query(Education).filter_by(profile_id=profile.id).delete()

        for edu in educations_data:
            education = Education(
                profile_id=profile.id,
                institution=edu.get("institution"),
                degree=edu.get("degree"),
                field_of_study=edu.get("field_of_study"),
                from_year=edu.get("from_year"),
                to_year=edu.get("to_year"),
            )
            db.session.add(education)

        # Update User Preferences if provided
        preferences_data = data.get("preferences", {})
        preferences = UserPreferences.query.filter_by(profile_id=profile.id).first()

        if preferences:
            preferences.preferred_location = preferences_data.get(
                "preferred_location", preferences.preferred_location
            )
            preferences.full_time = preferences_data.get(
                "full_time", preferences.full_time
            )
            preferences.part_time = preferences_data.get(
                "part_time", preferences.part_time
            )
            preferences.remote = preferences_data.get("remote", preferences.remote)
        else:
            preferences = UserPreferences(
                profile_id=profile.id,
                preferred_location=preferences_data.get("preferred_location"),
                full_time=preferences_data.get("full_time", True),
                part_time=preferences_data.get("part_time", False),
                remote=preferences_data.get("remote", False),
            )
            db.session.add(preferences)

        skills = preferences_data.get("skills", [])
        categories = preferences_data.get("categories", [])

        preferences.remove_skills([skill.id for skill in preferences.skills])
        preferences.remove_categories(
            [category.id for category in preferences.categories]
        )

        preferences.add_skills(skills)
        preferences.add_categories(categories)

        # Commit the session to save all changes
        db.session.commit()

        return {"message": "Profile updated successfully"}, 200  # OK
