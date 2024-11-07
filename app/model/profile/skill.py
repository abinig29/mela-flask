from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.extension import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user_preferences = relationship(
        "UserPreferences",
        secondary="user_skill_association",
        back_populates="skills",
    )
    jobs = relationship(
        "Job", secondary="job_skills", back_populates="skills"
    )

    def __repr__(self):
        return f"<Skill {self.skill_name}>"
