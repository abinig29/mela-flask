from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Table,
    Integer,
    DateTime,
    Text,
    MetaData,
)
import enum

from sqlalchemy.orm import relationship
from app import db
import uuid
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID, BIGINT


# Association table for job and category relationships
job_categories_association = Table(
    "job_categories",
    db.metadata,
    Column("job_id", db.UUID(as_uuid=True), ForeignKey("jobs.id"), primary_key=True),
    Column(
        "category_id",
        db.UUID(as_uuid=True),
        ForeignKey("categories.id"),
        primary_key=True,
    ),
)


job_skills_association = Table(
    "job_skills",
    db.metadata,
    Column("job_id", db.UUID(as_uuid=True), ForeignKey("jobs.id"), primary_key=True),
    Column(
        "skill_id",
        db.UUID(as_uuid=True),
        ForeignKey("skills.id"),
        primary_key=True,
    ),
)


class JobType(enum.Enum):
    FULL_TIME = "Full-Time"
    PART_TIME = "Part-Time"
    CONTRACT = "Contract"
    INTERNSHIP = "Internship"
    TEMPORARY = "Temporary"


class ExperienceLevel(enum.Enum):
    ENTRY_LEVEL = "Entry Level"
    MID_LEVEL = "Mid Level"
    SENIOR_LEVEL = "Senior Level"
    DIRECTOR = "Director"
    EXECUTIVE = "Executive"


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(String(255), nullable=False)
    description = db.Column(Text, nullable=False)
    company_name = db.Column(String(255), nullable=False)
    location = db.Column(String(255), nullable=True)
    posted_date = db.Column(DateTime, default=lambda: datetime.now(timezone.utc))
    application_link = db.Column(String(255), nullable=True)
    company_id = Column(
        db.UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True
    )
    source = db.Column(String(255), nullable=True)

    experience_level = db.Column(db.Enum(ExperienceLevel), nullable=False)
    job_type = db.Column(db.Enum(JobType), nullable=False)

    skills = relationship(
        "Skill", secondary=job_skills_association, back_populates="jobs"
    )
    categories = relationship(
        "Category", secondary=job_categories_association, back_populates="jobs"
    )
    posted_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "company_name": self.company_name,
            "location": self.location,
            "application_link": self.application_link,
            "job_type": self.job_type.name,
            "experience_level": self.experience_level.name,
            "source": self.source,
            "posted_date": self.posted_date,
            "skills": [
                {"id": str(skill.id), "name": skill.name} for skill in self.skills
            ],
            "categories": [
                {"id": str(category.id), "name": category.name}
                for category in self.categories
            ],
        }


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    user_preferences = relationship(
        "UserPreferences",
        secondary="user_category_association",
        back_populates="categories",
    )
    jobs = relationship(
        "Job", secondary=job_categories_association, back_populates="categories"
    )
