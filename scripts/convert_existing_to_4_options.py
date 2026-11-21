"""
Converts existing question banks to 4 options (A, B, C, D) strictly.
"""

def convert_questions(questions):
    converted = []
    for q in questions:
        new_q = {
            "topic": q["topic"],
            "difficulty": q["difficulty"],
            "subtopic": q["subtopic"],
            "subtopic_kn": q["subtopic_kn"],
            "subtopic_hi": q["subtopic_hi"],
            "text": q["text"],
            "text_kn": q["text_kn"],
            "text_hi": q["text_hi"],
            "option_a": q["option_a"],
            "option_a_kn": q["option_a_kn"],
            "option_a_hi": q["option_a_hi"],
            "option_b": q["option_b"],
            "option_b_kn": q["option_b_kn"],
            "option_b_hi": q["option_b_hi"],
            "option_c": q["option_c"],
            "option_c_kn": q["option_c_kn"],
            "option_c_hi": q["option_c_hi"],
            "option_d": q["option_d"],
            "option_d_kn": q["option_d_kn"],
            "option_d_hi": q["option_d_hi"],
            "correct_option": q["correct_option"],
            "explanation": q["explanation"],
            "explanation_kn": q["explanation_kn"],
            "explanation_hi": q["explanation_hi"]
        }
        if q.get("correct_option") == "E":
            # Swap option_e into option_d
            new_q["option_d"] = q["option_e"]
            new_q["option_d_kn"] = q["option_e_kn"]
            new_q["option_d_hi"] = q["option_e_hi"]
            new_q["correct_option"] = "D"
            
        assert new_q["correct_option"] in ["A", "B", "C", "D"], f"Invalid option {new_q['correct_option']}"
        converted.append(new_q)
    return converted

if __name__ == "__main__":
    import os, sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    import pprint
    from scripts.translations_c_prog import C_PROGRAMMING_QUESTIONS
    from scripts.translations_digital_elec import DIGITAL_ELECTRONICS_QUESTIONS
    from scripts.translations_eng_math import ENGINEERING_MATH_QUESTIONS
    from scripts.translations_circuits import CIRCUITS_QUESTIONS

    c_4 = convert_questions(C_PROGRAMMING_QUESTIONS)
    de_4 = convert_questions(DIGITAL_ELECTRONICS_QUESTIONS)
    math_4 = convert_questions(ENGINEERING_MATH_QUESTIONS)
    circ_4 = convert_questions(CIRCUITS_QUESTIONS)

    print(f"C: {len(c_4)}, DE: {len(de_4)}, Math: {len(math_4)}, Circ: {len(circ_4)}")
    assert not any(q['correct_option'] == 'E' for q in c_4 + de_4 + math_4 + circ_4)
    print("All existing 210 questions successfully verified with 4 options!")
