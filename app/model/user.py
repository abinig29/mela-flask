import enum
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID, BIGINT
import uuid
from app.extension import db, bcrypt
from .profile import profile
from flask_login import UserMixin


class RoleType(enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class AccountStatus(enum.Enum):
    REGISTERED = "REGISTERED"
    VERIFIED = "VERIFIED"
    SUSPENDED = "SUSPENDED"


class AuthProvider(enum.Enum):
    CREDENTIAL = "CREDENTIAL"
    GOOGLE = "GOOGLE"
    FACEBOOK = "FACEBOOK"


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(120), unique=True, index=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(128))
    first_time_login = db.Column(db.Boolean, default=True)

    role = db.Column(db.Enum(RoleType), default=RoleType.USER)
    verification_code_hash = db.Column(db.String(128))
    verification_code_expires = db.Column(BIGINT)

    account_status = db.Column(db.Enum(AccountStatus), default=AccountStatus.REGISTERED)
    active = db.Column(db.Boolean, default=True)
    auth_provider = db.Column(db.Enum(AuthProvider), default=AuthProvider.CREDENTIAL)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    # updated_at = db.Column(
    #     db.DateTime,
    #     default=lambda: datetime.now(timezone.utc),
    #     onupdate=lambda: datetime.now(timezone.utc),
    # )

    profile = db.relationship(
        "Profile", back_populates="user", uselist=False, cascade="all, delete"
    )
    company = db.relationship(
        "Company", backref="user", uselist=False, cascade="all, delete"
    )

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def set_verification_code(self, code):
        """Hash the verification code and store it."""
        self.verification_code_hash = bcrypt.generate_password_hash(code).decode(
            "utf-8"
        )

    def check_verification_code(self, code):
        """Check if the given verification code matches the hashed version."""
        return bcrypt.check_password_hash(self.verification_code_hash, code)

    def __repr__(self):
        return f"<User {self.username}>"
