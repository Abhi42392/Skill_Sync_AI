def calculate_skill_gap_score(
    resource_skill_ids,
    missing_skill_ids
):
    """
    Calculate how relevant a resource is
    to the learner's missing skills.
    """

    if not resource_skill_ids or not missing_skill_ids:
        return 0.0

    resource_skills = set(resource_skill_ids)
    missing_skills = set(missing_skill_ids)

    matched_skills = resource_skills.intersection(missing_skills)

    return len(matched_skills) / len(resource_skills)


def calculate_difficulty_score(
    difficulty: str,
    average_proficiency: float
):
    """
    Calculate how suitable the resource difficulty
    is for the learner.
    """

    difficulty_levels = {
        "beginner": 0.25,
        "intermediate": 0.50,
        "advanced": 0.75,
    }

    resource_level = difficulty_levels.get(
        difficulty.lower(),
        0.50
    )

    difference = abs(
        resource_level - average_proficiency
    )

    score = 1.0 - difference

    return max(0.0, min(1.0, score))

def calculate_prerequisite_score(
    prerequisite_skill_ids,
    user_skill_proficiencies
):
    """
    Calculate whether the learner has the skills
    required to start the resource.
    """

    if not prerequisite_skill_ids:
        return 1.0

    if not user_skill_proficiencies:
        return 0.0

    total_score = 0.0

    for skill_id in prerequisite_skill_ids:
        proficiency = user_skill_proficiencies.get(
            skill_id,
            0.0
        )

        # 0.5 proficiency is considered sufficient
        total_score += min(proficiency / 0.5, 1.0)

    return total_score / len(prerequisite_skill_ids)

def calculate_score(
    semantic_similarity: float,
    skill_gap_score: float = 0.0,
    prerequisite_score: float = 1.0,
    difficulty_score: float = 1.0,
    preference_score: float = 0.0,
):
    """
    Calculate final hybrid recommendation score.
    """

    return (
        0.35 * semantic_similarity
        + 0.25 * skill_gap_score
        + 0.20 * prerequisite_score
        + 0.10 * difficulty_score
        + 0.10 * preference_score
    )