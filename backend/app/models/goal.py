from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    Text,
)

from app.db.database import Base


class Goal(Base):
    __tablename__ = "goals"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    title = Column(
        String(255),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    priority = Column(
        String(20),
        default="medium",
    )

    target_date = Column(
        Date,
        nullable=True,
    )

    status = Column(
        String(20),
        default="active",
    )