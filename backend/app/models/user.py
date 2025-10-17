from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, IDMixin, TimestampMixin


class User(SQLAlchemyBaseUserTable[int], Base, IDMixin, TimestampMixin):
    """User model for authentication and user management"""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(1024),
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=False)

    # Additional fields
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Credits system
    credits: Mapped[float] = mapped_column(
        Float,
        default=10.0,  # 무료 체험 10 크레딧
        nullable=False
    )

    # Relationships
    projects: Mapped[list["Project"]] = relationship(
        "Project",
        back_populates="user",
        cascade="all, delete-orphan"
    )
