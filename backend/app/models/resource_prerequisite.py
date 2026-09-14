from sqlalchemy import Column, ForeignKey, Integer
from app.db.database import Base


class ResourcePrerequisite(Base):
    __tablename__ = "resource_prerequisites"

    id = Column(Integer, primary_key=True, index=True)

    resource_id = Column(
        Integer,
        ForeignKey("resources.id"),
        nullable=False
    )

    skill_id = Column(
        Integer,
        ForeignKey("skills.id"),
        nullable=False
    )