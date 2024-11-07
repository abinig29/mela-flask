from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from app.extension import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Experience(db.Model):
    __tablename__ = "experiences"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = db.Column(db.UUID(as_uuid=True),  ForeignKey("profiles.id"), nullable=False)

    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=True)
    remarks = db.Column(db.Text, nullable=True)
    created_at = db.Column(DateTime, default=lambda: datetime.now(timezone.utc))
    # updated_at = db.Column(
    #     DateTime,
    #     default=lambda: datetime.now(timezone.utc),
    #     onupdate=lambda: datetime.now(timezone.utc),
    # )

    profile = relationship("Profile", back_populates="experiences")

    def __repr__(self):
        return f"<Experience {self.company} - {self.role}>"
