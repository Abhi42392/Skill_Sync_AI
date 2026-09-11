from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
)

from app.db.database import Base


class UserSkill(Base):
    __tablename__ = "user_skills"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    skill_id = Column(
        Integer,
        ForeignKey("skills.id"),
        nullable=False,
    )

    proficiency = Column(
        Float,
        default=0.0,
    )