from sqlalchemy import (
    Column,
    Float,
    Integer,
    String,
    Text,
)

from pgvector.sqlalchemy import Vector

from app.core.config import settings
from app.db.database import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    title = Column(
        String(255),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=False,
    )

    resource_type = Column(
        String(50),
        nullable=False,
    )

    difficulty = Column(
        String(50),
        nullable=False,
    )

    duration_hours = Column(
        Float,
        nullable=True,
    )

    url = Column(
        Text,
        nullable=True,
    )

    embedding = Column(
        Vector(settings.EMBEDDING_DIM),
        nullable=True,
    )