from app.db.database import SessionLocal
from app.models.resource import Resource
from app.embeddings.embedder import embed_text


def generate_resource_embeddings():
    db = SessionLocal()

    try:
        resources = db.query(Resource).all()

        for resource in resources:
            text = f"{resource.title}. {resource.description}"

            resource.embedding = embed_text(text)

        db.commit()

        print(f"Generated embeddings for {len(resources)} resources.")

    finally:
        db.close()


if __name__ == "__main__":
    generate_resource_embeddings()