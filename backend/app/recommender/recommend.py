from app.db.database import SessionLocal
from app.models.resource_skill import ResourceSkill
from app.models.user_skill import UserSkill
from app.embeddings.vector_search import search_resources
from app.recommender.scorer import (
    calculate_score,
    calculate_skill_gap_score,
    calculate_difficulty_score,
    calculate_prerequisite_score,
)
from app.models.resource_prerequisite import ResourcePrerequisite

def get_missing_skill_ids(db, user_id: int):
    """
    Return skill IDs where the learner's proficiency
    is below 0.5.
    """

    user_skills = (
        db.query(UserSkill)
        .filter(UserSkill.user_id == user_id)
        .all()
    )

    return [
        user_skill.skill_id
        for user_skill in user_skills
        if user_skill.proficiency < 0.5
    ]


def recommend_resources(
    user_id: int,
    goal: str,
    limit: int = 5
):
    db = SessionLocal()

    try:
        # Get learner's skills
        user_skills = (
            db.query(UserSkill)
            .filter(UserSkill.user_id == user_id)
            .all()
        )

        # Find missing skills
        missing_skill_ids = get_missing_skill_ids(
            db,
            user_id
        )

        # Calculate average proficiency
        average_proficiency = (
            sum(skill.proficiency for skill in user_skills)
            / len(user_skills)
            if user_skills
            else 0.0
        )

        # Semantic vector search
        resources = search_resources(
            goal,
            limit
        )

        recommendations = []

        for resource in resources:

    # Skills taught by this resource
            resource_skill_ids = [
                row.skill_id
                for row in (
                    db.query(ResourceSkill)
                    .filter(
                        ResourceSkill.resource_id == resource.id
                    )
                    .all()
                )
            ]

            # Calculate skill-gap score
            skill_gap_score = calculate_skill_gap_score(
                resource_skill_ids,
                missing_skill_ids
            )

            # Get prerequisites for this resource
            prerequisite_skill_ids = [
                row.skill_id
                for row in (
                    db.query(ResourcePrerequisite)
                    .filter(
                        ResourcePrerequisite.resource_id == resource.id
                    )
                    .all()
                )
            ]

    # Convert learner skills into {skill_id: proficiency}
            user_skill_proficiencies = {
                skill.skill_id: skill.proficiency
                for skill in user_skills
            }

            # Calculate prerequisite score
            prerequisite_score = calculate_prerequisite_score(
                prerequisite_skill_ids,
                user_skill_proficiencies
            )

            # Calculate difficulty score
            difficulty_score = calculate_difficulty_score(
                resource.difficulty,
                average_proficiency
            )

            # Final hybrid score
            final_score = calculate_score(
                semantic_similarity=resource.similarity,
                skill_gap_score=skill_gap_score,
                prerequisite_score=prerequisite_score,
                difficulty_score=difficulty_score,
                preference_score=0.0,
            )

            recommendations.append({
                "id": resource.id,
                "title": resource.title,
                "description": resource.description,
                "difficulty": resource.difficulty,
                "similarity": resource.similarity,
                "skill_gap_score": skill_gap_score,
                "prerequisite_score": prerequisite_score,
                "difficulty_score": difficulty_score,
                "score": final_score,
            })

        # Highest score first
        recommendations.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return recommendations

    finally:
        db.close()


if __name__ == "__main__":

    user_id = int(input("Enter user ID: "))
    goal = input("Enter your learning goal: ")

    results = recommend_resources(
        user_id=user_id,
        goal=goal
    )

    print("\nRecommended Resources:\n")

    for resource in results:
        print(
            f"{resource['title']} | "
            f"Difficulty: {resource['difficulty']} | "
            f"Similarity: {resource['similarity']:.4f} | "
            f"Skill Gap: {resource['skill_gap_score']:.4f} | "
            f"Prerequisite: {resource['prerequisite_score']:.4f} | "
            f"Difficulty Score: {resource['difficulty_score']:.4f} | "
            f"Final Score: {resource['score']:.4f}"
        )