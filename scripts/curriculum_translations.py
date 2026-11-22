"""
Master Curriculum Translations Aggregator (Strict 4-Option Architecture)
=======================================================================
Combines all 364 VTU Engineering Questions across 14 syllabus topics (26 per topic >= 25):
- 210 existing questions converted strictly to 4 options (A-D)
- 154 expanded questions with authentic English, Kannada, and Hindi translations
"""

import os
import sys
from collections import Counter

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.translations_c_prog import C_PROGRAMMING_QUESTIONS
from scripts.translations_digital_elec import DIGITAL_ELECTRONICS_QUESTIONS
from scripts.translations_eng_math import ENGINEERING_MATH_QUESTIONS
from scripts.translations_circuits import CIRCUITS_QUESTIONS

from scripts.expanded_c_prog import EXPANDED_C_QUESTIONS
from scripts.expanded_digital_elec import EXPANDED_DE_QUESTIONS
from scripts.expanded_eng_math import EXPANDED_MATH_QUESTIONS
from scripts.expanded_circuits import EXPANDED_CIRCUITS_QUESTIONS

EXISTING_4_OPTIONS = (
    C_PROGRAMMING_QUESTIONS +
    DIGITAL_ELECTRONICS_QUESTIONS +
    ENGINEERING_MATH_QUESTIONS +
    CIRCUITS_QUESTIONS
)

EXPANDED_4_OPTIONS = (
    EXPANDED_C_QUESTIONS +
    EXPANDED_DE_QUESTIONS +
    EXPANDED_MATH_QUESTIONS +
    EXPANDED_CIRCUITS_QUESTIONS
)

ALL_CURRICULUM_QUESTIONS = EXISTING_4_OPTIONS + EXPANDED_4_OPTIONS


def validate_curriculum_questions():
    """Validates that all 364 questions have strictly 4 options (A-D), 25+ per topic, and clean translations."""
    total = len(ALL_CURRICULUM_QUESTIONS)
    assert total == 364, f"Expected 364 questions, found {total}"

    forbidden_placeholders = [
        "(ಕನ್ನಡ ರೂಪಾಂತರ)",
        "(हिंदी अनुवाद)",
        "ಮೇಲಿನ ಯಾವುದೂ ಅಲ್ಲ",
        "None of the above"
    ]

    required_keys = [
        "topic", "difficulty",
        "subtopic", "subtopic_kn", "subtopic_hi",
        "text", "text_kn", "text_hi",
        "option_a", "option_a_kn", "option_a_hi",
        "option_b", "option_b_kn", "option_b_hi",
        "option_c", "option_c_kn", "option_c_hi",
        "option_d", "option_d_kn", "option_d_hi",
        "correct_option",
        "explanation", "explanation_kn", "explanation_hi"
    ]

    topic_counts = Counter()

    for idx, q in enumerate(ALL_CURRICULUM_QUESTIONS):
        for k in required_keys:
            assert k in q and q[k], f"Question {idx} ({q.get('topic')}) missing or empty key: {k}"
            val = str(q[k])
            for forbidden in forbidden_placeholders:
                assert forbidden not in val, f"Question {idx} key '{k}' contains forbidden placeholder '{forbidden}': {val[:80]}"

        assert q["correct_option"] in ["A", "B", "C", "D"], f"Question {idx} has invalid correct_option: {q['correct_option']}"
        assert q["difficulty"] in ["easy", "medium", "hard"], f"Question {idx} has invalid difficulty: {q['difficulty']}"
        topic_counts[q["topic"]] += 1

    print("\n--- Topic Question Counts (Target: >= 25 per topic) ---")
    for topic, count in sorted(topic_counts.items()):
        print(f"  • {topic}: {count} questions")
        assert count >= 25, f"Topic '{topic}' has fewer than 25 questions: {count}"

    assert len(topic_counts) == 14, f"Expected 14 topics, got {len(topic_counts)}"
    print(f"\nAll {total} questions across all 14 topics strictly adhere to the 4-option (A-D) architecture with complete trilingual support!")


if __name__ == "__main__":
    validate_curriculum_questions()
