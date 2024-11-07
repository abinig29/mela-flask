from app.extension import db
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Education(db.Model):
    __tablename__ = "educations"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = db.Column(db.UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False)

    institution = db.Column(
        db.String(100), nullable=False
    ) 
    degree = db.Column(
        db.String(100), nullable=False
    ) 
    field_of_study = db.Column(
        db.String(100), nullable=True
    )  
    from_year = db.Column(db.Integer, nullable=False)  
    to_year = db.Column(db.Integer, nullable=False) 
    created_at = db.Column(DateTime, default=lambda: datetime.now(timezone.utc))
    # updated_at = db.Column(
    #     DateTime,
    #     default=lambda: datetime.now(timezone.utc),
    #     onupdate=lambda: datetime.now(timezone.utc),
    # )

    profile = relationship("Profile", back_populates="educations")

    def __repr__(self):
        return f"<Education {self.institution} - {self.degree}>"
