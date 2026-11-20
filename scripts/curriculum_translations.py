"""
Master Curriculum Translations Aggregator
========================================
Combines all 210 VTU Engineering Questions with complete English, Kannada (kn), and Hindi (hi) translations:
- C Programming (60 questions, Topics 1-4)
- Digital Electronics (60 questions, Topics 5-8)
- Engineering Mathematics (45 questions, Topics 9-11)
- Basic Circuit Analysis (45 questions, Topics 12-14)
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.translations_c_prog import C_PROGRAMMING_QUESTIONS
from scripts.translations_digital_elec import DIGITAL_ELECTRONICS_QUESTIONS
from scripts.translations_eng_math import ENGINEERING_MATH_QUESTIONS
from scripts.translations_circuits import CIRCUITS_QUESTIONS

ALL_CURRICULUM_QUESTIONS = (
    C_PROGRAMMING_QUESTIONS +
    DIGITAL_ELECTRONICS_QUESTIONS +
    ENGINEERING_MATH_QUESTIONS +
    CIRCUITS_QUESTIONS
)

def validate_curriculum_questions():
    """Validates that all 210 questions have complete, clean parallel translations without placeholders."""
    total = len(ALL_CURRICULUM_QUESTIONS)
    assert total == 210, f"Expected 210 questions, found {total}"

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
        "option_e", "option_e_kn", "option_e_hi",
        "correct_option",
        "explanation", "explanation_kn", "explanation_hi"
    ]

    for idx, q in enumerate(ALL_CURRICULUM_QUESTIONS):
        for k in required_keys:
            assert k in q and q[k], f"Question {idx} ({q.get('topic')}) missing or empty key: {k}"
            val = str(q[k])
            for forbidden in forbidden_placeholders:
                assert forbidden not in val, f"Question {idx} key '{k}' contains forbidden placeholder '{forbidden}': {val[:80]}"

        assert q["correct_option"] in ["A", "B", "C", "D", "E"], f"Question {idx} has invalid correct_option: {q['correct_option']}"
        assert q["difficulty"] in ["easy", "medium", "hard"], f"Question {idx} has invalid difficulty: {q['difficulty']}"

    print(f"Validation successful: All {total} questions across 14 syllabus topics are complete and clean.")

if __name__ == "__main__":
    validate_curriculum_questions()
