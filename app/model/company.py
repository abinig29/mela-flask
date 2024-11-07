from sqlalchemy import Column, String, Integer, ForeignKey
from app import db
import uuid
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID


class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    website = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True)
    jobs = db.relationship("Job", backref="company", cascade="all, delete-orphan")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    def to_dict(self):
        company_data = {
            "id": str(self.id),
            "name": self.name,
            "jobs_count": len(self.jobs),
        }
        if self.email:
            company_data["email"] = self.email
        if self.website:
            company_data["website"] = self.website
        if self.location:
            company_data["location"] = self.location
        
        return company_data
    def __repr__(self):
        return f"<Company {self.name}>"
