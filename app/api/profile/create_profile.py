from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extension import db
from app.model import Profile, Experience, Education, UserPreferences, Skill, Category


class CreateProfile(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()["id"]
        data = request.json

        existing_profile = Profile.query.filter_by(user_id=current_user_id).first()
        if existing_profile:
            return {
                "message": "A profile already exists for this user."
            }, 400  # Bad Request

        # Create the Profile
        profile = Profile(
            user_id=current_user_id,
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            date_of_birth=data.get("date_of_birth"),
            phone_number=data.get("phone_number"),
            address_line_1=data.get("address_line_1"),
            city=data.get("city"),
            state=data.get("state"),
            country=data.get("country"),
            website=data.get("website"),
            linkedin_profile=data.get("linkedin_profile"),
            github_profile=data.get("github_profile"),
        )

        # Add the profile to the session
        db.session.add(profile)
        db.session.flush()  # Flush to get the profile ID

        # Create Experiences if provided
        experiences_data = data.get("experiences", [])
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

        # Create Education if provided
        educations_data = data.get("educations", [])
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

        # Create User Preferences if provided
        preferences_data = data.get("preferences", {})
        preferences = UserPreferences(
            profile_id=profile.id,
            preferred_location=preferences_data.get("preferred_location"),
            full_time=preferences_data.get("full_time", True),
            part_time=preferences_data.get("part_time", False),
            remote=preferences_data.get("remote", False),
        )
        db.session.add(preferences)
        db.session.flush()  # Flush to get the preferences ID

        # Add skills and categories to preferences
        skills = preferences_data.get("skills", [])
        categories = preferences_data.get("categories", [])
        print("skills", skills)
        print("categories", categories)

        preferences.add_skills(skills)
        preferences.add_categories(categories)

        # Commit the session to save all changes
        db.session.commit()

        return {
            "message": "Profile created successfully",
        }, 201
