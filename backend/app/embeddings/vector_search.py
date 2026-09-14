from sqlalchemy import text

from app.db.database import SessionLocal
from app.embeddings.embedder import embed_text


def search_resources(query: str, limit: int = 5):
    query_embedding = embed_text(query)

    db = SessionLocal()

    try:
        sql = text("""
            SELECT
                id,
                title,
                description,
                difficulty,
                url,
                1 - (embedding <=> CAST(:embedding AS vector)) AS similarity
            FROM resources
            WHERE embedding IS NOT NULL
            ORDER BY embedding <=> CAST(:embedding AS vector)
            LIMIT :limit
        """)

        results = db.execute(
            sql,
            {
                "embedding": str(query_embedding),
                "limit": limit,
            },
        ).fetchall()

        return results

    finally:
        db.close()


if __name__ == "__main__":
    query = input("Enter your learning goal: ")

    results = search_resources(query)

    for result in results:
        print(
            f"{result.title} | "
            f"Similarity: {result.similarity:.4f}"
        )