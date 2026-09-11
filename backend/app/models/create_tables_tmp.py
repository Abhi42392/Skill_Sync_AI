from sqlalchemy import text

from app.db.database import Base, engine

# Import models so SQLAlchemy knows about them.
from app.models import (
    User,
    Goal,
    Skill,
    UserSkill,
    Resource,
)


def main():
    with engine.begin() as connection:
        connection.execute(
            text("CREATE EXTENSION IF NOT EXISTS vector")
        )

    Base.metadata.create_all(bind=engine)

    print("Database tables created successfully.")


if __name__ == "__main__":
    main()