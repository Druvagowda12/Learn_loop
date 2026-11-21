"""
Learnloop Adaptation Engine (Rule-based)
========================================
Implements transparent, explainable scoring, mastery bands, difficulty mix selection,
and personalized study recommendations for VTU engineering students.
"""

from typing import List, Dict, Any, Optional

# Mastery Band Thresholds
BAND_LOW_MAX = 39.99
BAND_MEDIUM_MIN = 40.0
BAND_MEDIUM_MAX = 74.99
BAND_HIGH_MIN = 75.0

# Difficulty Mix Configurations (total = 10 questions)
MIX_EASY_HEAVY = {'easy': 6, 'medium': 3, 'hard': 1}
MIX_BALANCED = {'easy': 3, 'medium': 4, 'hard': 3}
MIX_HARD_HEAVY = {'easy': 1, 'medium': 4, 'hard': 5}


def compute_attempt_score(results: List[Dict[str, Any]]) -> float:
    """
    Computes percentage score from a list of answer results.
    Each result must have 'is_correct' (bool).
    """
    if not results:
        return 0.0
    correct_count = sum(1 for r in results if r.get('is_correct'))
    return round((correct_count / len(results)) * 100.0, 1)


def get_mastery_band(score_pct: float) -> str:
    """
    Returns the mastery level string ('Low', 'Medium', 'High') for a given percentage.
    """
    if score_pct < 40.0:
        return 'Low'
    elif score_pct < 75.0:
        return 'Medium'
    else:
        return 'High'


def topic_mastery(attempts: List[Any]) -> Dict[str, Any]:
    """
    Calculates weighted average of up to 3 most recent attempts.
    Attempts should be ordered chronologically (most recent last, or passed in order).
    Weights prioritize recency:
      - 1 attempt: 1.0
      - 2 attempts: [0.35, 0.65] (recent gets 65%)
      - 3 attempts: [0.20, 0.30, 0.50] (recent gets 50%)
    """
    if not attempts:
        return {
            'mastery_pct': 0.0,
            'mastery_level': 'Low',
            'attempts_count': 0
        }

    # Extract score values (supports objects with .score_pct or raw dict/float)
    scores = []
    for att in attempts[-3:]:
        if hasattr(att, 'score_pct'):
            scores.append(float(att.score_pct))
        elif isinstance(att, dict) and 'score_pct' in att:
            scores.append(float(att['score_pct']))
        elif isinstance(att, (int, float)):
            scores.append(float(att))

    if not scores:
        return {'mastery_pct': 0.0, 'mastery_level': 'Low', 'attempts_count': 0}

    count = len(scores)
    if count == 1:
        weighted_score = scores[0]
    elif count == 2:
        weighted_score = scores[0] * 0.35 + scores[1] * 0.65
    else:
        weighted_score = scores[0] * 0.20 + scores[1] * 0.30 + scores[2] * 0.50

    weighted_score = round(weighted_score, 1)
    band = get_mastery_band(weighted_score)

    return {
        'mastery_pct': weighted_score,
        'mastery_level': band,
        'attempts_count': len(attempts)
    }


def next_difficulty(mastery_level: str, last_score: Optional[float] = None) -> Dict[str, int]:
    """
    Selects question difficulty mix based on topic mastery and last score trend.
    Stepping rule:
      - If last score is high (>= 80%), shift upward.
      - If last score is low (< 40%), shift downward.
    """
    level = (mastery_level or 'Low').capitalize()

    # Step-down if last score was severely low
    if last_score is not None and last_score < 40.0:
        return dict(MIX_EASY_HEAVY)

    # Step-up if last score was very high
    if last_score is not None and last_score >= 80.0 and level != 'Low':
        return dict(MIX_HARD_HEAVY)

    if level == 'Low':
        return dict(MIX_EASY_HEAVY)
    elif level == 'Medium':
        return dict(MIX_BALANCED)
    else:  # High
        return dict(MIX_HARD_HEAVY)


def recommend(topic_name: str, mastery_level: str, score_pct: float, missed_subtopics: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Generates rule-based recommendations tailored to student mastery band,
    including an explainable reason.
    """
    missed_subtopics = missed_subtopics or []
    subtopics_str = ", ".join(missed_subtopics) if missed_subtopics else None
    level = (mastery_level or 'Low').capitalize()

    if level == 'Low':
        action_headline = "Fundamental Concept Revision Required"
        reason = (
            f"You scored {score_pct:.0f}% on {topic_name}. At this foundational stage, "
            "we suggest starting with structured concept notes, watching a verified video walkthrough, "
            "and solving an easy practice set before retrying the quiz."
        )
        if subtopics_str:
            reason += f" Pay special attention to: {subtopics_str}."

        recommended_sequence = ['notes', 'video', 'practice']
        advice = "Revise foundational notes and watch video illustrations before your next quiz attempt."

    elif level == 'Medium':
        action_headline = "Strengthen Applied Problem Solving"
        reason = (
            f"You scored {score_pct:.0f}% on {topic_name}. You have a solid grasp of basics, "
            "but need further practice with worked numericals and edge cases to reach high mastery."
        )
        if subtopics_str:
            reason += f" Review targeted notes on: {subtopics_str}."

        recommended_sequence = ['example', 'notes', 'practice']
        advice = "Work through step-by-step example solutions and try the intermediate practice problem set."

    else:  # High
        action_headline = "High Mastery Achieved — Advance to Challenges"
        reason = (
            f"Congratulations on scoring {score_pct:.0f}% on {topic_name}! You have demonstrated "
            "strong subject competence. We recommend challenging yourself with advanced practice sets "
            "or progressing to subsequent engineering syllabus topics."
        )
        recommended_sequence = ['practice', 'example']
        advice = "Solve higher-order thinking problems and move ahead to the next syllabus module."

    return {
        'mastery_level': level,
        'action_headline': action_headline,
        'reason': reason,
        'recommended_sequence': recommended_sequence,
        'advice': advice,
        'missed_subtopics': missed_subtopics
    }
