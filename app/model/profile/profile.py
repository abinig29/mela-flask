from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.extension import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    address_line_1 = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), nullable=True)

    website = db.Column(db.String(100), nullable=True)
    linkedin_profile = db.Column(db.String(100), nullable=True)
    github_profile = db.Column(db.String(100), nullable=True)

    cv_link = db.Column(db.String(255), nullable=True)

    created_at = db.Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="profile")

    experiences = relationship(
        "Experience", back_populates="profile", cascade="all, delete-orphan"
    )
    educations = relationship(
        "Education", back_populates="profile", cascade="all, delete-orphan"
    )
    preferences = relationship(
        "UserPreferences", back_populates="profile", uselist=False
    )

    def __repr__(self):
        return f"<Profile {self.first_name} {self.last_name}>"
