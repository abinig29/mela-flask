from app import db, create_app  # Assuming you have a factory function called create_app
from app.model import Job, Skill, Category, ExperienceLevel, JobType
from datetime import datetime, timezone
import uuid

# Sample data for seeding
jobs_data = [
    {
        "title": "Software Engineer",
        "description": "Develop and maintain web applications.",
        "company_name": "Tech Solutions",
        "location": "New York, NY",
        "experience_level": ExperienceLevel.MID_LEVEL,
        "job_type": JobType.FULL_TIME,
        "skills": ["Python", "SQL", "Flask"],
        "categories": ["Engineering", "Technology"],
    },
    {
        "title": "Data Scientist",
        "description": "Analyze and interpret complex data.",
        "company_name": "DataCorp",
        "location": "San Francisco, CA",
        "experience_level": ExperienceLevel.SENIOR_LEVEL,
        "job_type": JobType.FULL_TIME,
        "skills": ["Python", "Machine Learning", "Data Analysis"],
        "categories": ["Data Science", "Engineering"],
    },
]


def seed_jobs():
    for job_data in jobs_data:
        # Create or fetch existing skills
        skills = []
        for skill_name in job_data["skills"]:
            skill = Skill.query.filter_by(name=skill_name).first()
            if not skill:
                skill = Skill(name=skill_name)
                db.session.add(skill)
            skills.append(skill)

        # Create or fetch existing categories
        categories = []
        for category_name in job_data["categories"]:
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name)
                db.session.add(category)
            categories.append(category)

        # Create the Job instance
        job = Job(
            title=job_data["title"],
            description=job_data["description"],
            company_name=job_data["company_name"],
            location=job_data["location"],
            posted_date=datetime.now(timezone.utc),
            experience_level=job_data["experience_level"],
            job_type=job_data["job_type"],
            skills=skills,
            categories=categories,
        )

        db.session.add(job)

    db.session.commit()
    print("Jobs seeded successfully.")


# Run the seeder function within an app context
if __name__ == "__main__":
    app = create_app()  # Initialize the Flask app using the factory function
    with app.app_context():
        db.create_all()  # Ensures tables are created
        seed_jobs()
