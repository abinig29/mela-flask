from sqlalchemy import Column, String, Boolean, ForeignKey, Table, MetaData
from sqlalchemy.orm import relationship
from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.model.job import Category
from app.model.profile.skill import Skill


# Define metadata
metadata = MetaData()

# Define user-category association table
user_category_association = Table(
    "user_category_association",
    db.metadata,
    db.Column(
        "user_preferences_id",
        db.UUID(as_uuid=True),
        ForeignKey("user_preferences.id"),
        primary_key=True,
    ),
    db.Column(
        "category_id",
        db.UUID(as_uuid=True),
        ForeignKey("categories.id"),
        primary_key=True,
    ),
)

# Define user-skill association table
user_skill_association = Table(
    "user_skill_association",
    db.metadata,
    db.Column(
        "user_preferences_id",
        db.UUID(as_uuid=True),
        ForeignKey("user_preferences.id"),
        primary_key=True,
    ),
    db.Column(
        "skill_id", db.UUID(as_uuid=True), ForeignKey("skills.id"), primary_key=True
    ),
)


# Define UserPreferences model
class UserPreferences(db.Model):
    __tablename__ = "user_preferences"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(
        db.UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False
    )

    preferred_location = Column(String)
    full_time = Column(Boolean, default=True)
    part_time = Column(Boolean, default=False)
    remote = Column(Boolean, default=False)

    categories = relationship(
        "Category",
        secondary=user_category_association,
        back_populates="user_preferences",
    )

    skills = relationship(
        "Skill", secondary=user_skill_association, back_populates="user_preferences"
    )
    profile = relationship("Profile", back_populates="preferences")

    def add_skills(self, skill_ids):
        """Add skills by their IDs."""
        for skill_id in skill_ids:
            skill = Skill.query.get(skill_id)
            print(skill)
            if skill and skill not in self.skills:
                self.skills.append(skill)

    def remove_skills(self, skill_ids):
        """Remove skills by their IDs."""
        for skill_id in skill_ids:
            skill = Skill.query.get(skill_id)
            if skill in self.skills:
                self.skills.remove(skill)

    def add_categories(self, category_ids):
        """Add categories by their IDs."""
        for category_id in category_ids:
            category = Category.query.get(category_id)
            print(category)
            if category and category not in self.categories:
                self.categories.append(category)

    def remove_categories(self, category_ids):
        """Remove categories by their IDs."""
        for category_id in category_ids:
            category = Category.query.get(category_id)
            if category in self.categories:
                self.categories.remove(category)
