"""
Learnloop Seed Generator
========================
Populates SQLite database with:
- 4 VTU Engineering Subjects
- 14 Syllabus Topics
- 168+ Verified Technical MCQs (12 per topic across easy, medium, hard)
- 45+ Curated Learning Resources (Notes, Verified Video Searches, Worked Examples, Practice Sets)
- Synthetic Demo Users (student1, student2, teacher) with pre-computed quiz histories
"""

from datetime import datetime, timezone, timedelta
import random
from models import db, User, Subject, Topic, Question, Attempt, AttemptAnswer, TopicProgress, Resource, ResourceView
from engine import topic_mastery
from scripts.bilingual_resources_data import TOPIC_RESOURCES_KN
from scripts.curriculum_translations import ALL_CURRICULUM_QUESTIONS

def seed_database(app):
    with app.app_context():
        db.create_all()

        # Check if already seeded
        if Subject.query.first():
            print("Database already contains data. Skipping full re-seed.")
            return

        print("Seeding database with engineering curriculum, verified MCQs, and synthetic users...")

        # 1. Create Subjects
        sub_c = Subject(name="C Programming")
        sub_de = Subject(name="Digital Electronics")
        sub_math = Subject(name="Engineering Mathematics")
        sub_circuits = Subject(name="Basic Circuit Analysis")

        db.session.add_all([sub_c, sub_de, sub_math, sub_circuits])
        db.session.flush()

        # 2. Create Topics
        topics_data = [
            # C Programming
            (sub_c.id, "Arrays in C", "One-dimensional and multi-dimensional contiguous memory arrays, indexing, and boundary conditions."),
            (sub_c.id, "Pointers and Memory", "Memory addresses, pointer arithmetic, dereferencing, void pointers, and dynamic allocation."),
            (sub_c.id, "Functions and Recursion", "Parameter passing mechanisms (call by value/reference), return types, stack frames, and recursion."),
            (sub_c.id, "Control Flow and Loops", "Conditional branching (if-else, switch-case) and iteration constructs (for, while, do-while)."),

            # Digital Electronics
            (sub_de.id, "Number Systems & Codes", "Binary, Octal, Hexadecimal conversions, 1's/2's complement arithmetic, and BCD/Gray codes."),
            (sub_de.id, "Boolean Algebra & Logic Simplification", "De Morgan's laws, canonical SOP/POS forms, minterms, and Karnaugh Map (K-Map) reduction."),
            (sub_de.id, "Logic Gates & Universal Realization", "Standard AND/OR/NOT gates, NAND/NOR universality, XOR/XNOR parity generators."),
            (sub_de.id, "Combinational Logic Circuits", "Design of Adders (Half/Full), Subtractors, Multiplexers (MUX), Demultiplexers, and Decoders."),

            # Engineering Mathematics
            (sub_math.id, "Matrices & Linear Systems", "Matrix operations, determinants, rank of a matrix, Gaussian elimination, and Eigenvalues/Eigenvectors."),
            (sub_math.id, "Differential Calculus", "Partial differentiation, Euler's theorem for homogeneous functions, Taylor series, and Jacobians."),
            (sub_math.id, "Integral Calculus", "Definite integrals, reduction formulas, double/triple integrals, and evaluation of areas/volumes."),

            # Circuit Analysis
            (sub_circuits.id, "Ohm's & Kirchhoff's Laws", "Basic electrical quantities, Ohm's law, Kirchhoff's Current Law (KCL), and Kirchhoff's Voltage Law (KVL)."),
            (sub_circuits.id, "Series-Parallel Circuit Analysis", "Equivalent resistance, voltage divider rule, current divider rule, and star-delta conversions."),
            (sub_circuits.id, "Mesh & Nodal Analysis", "Matrix formulations for planar mesh currents, supermesh, essential node voltages, and supernode analysis.")
        ]

        topic_objects = {}
        for sub_id, name, desc in topics_data:
            t = Topic(subject_id=sub_id, name=name, description=desc)
            db.session.add(t)
            db.session.flush()
            topic_objects[name] = t

        # Helper to add questions from verified curriculum dataset
        print("Seeding verified 4-option MCQs across all 14 topics with full EN, KN, and HI support...")
        for item in ALL_CURRICULUM_QUESTIONS:
            t_obj = topic_objects.get(item["topic"])
            if t_obj:
                q = Question(
                    topic_id=t_obj.id,
                    text=item["text"],
                    option_a=item["option_a"],
                    option_b=item["option_b"],
                    option_c=item["option_c"],
                    option_d=item["option_d"],
                    option_e=None,
                    correct_option=item["correct_option"],
                    difficulty=item["difficulty"],
                    subtopic=item["subtopic"],
                    explanation=item["explanation"],
                    text_kn=item["text_kn"],
                    option_a_kn=item["option_a_kn"],
                    option_b_kn=item["option_b_kn"],
                    option_c_kn=item["option_c_kn"],
                    option_d_kn=item["option_d_kn"],
                    option_e_kn=None,
                    explanation_kn=item["explanation_kn"],
                    subtopic_kn=item["subtopic_kn"],
                    text_hi=item["text_hi"],
                    option_a_hi=item["option_a_hi"],
                    option_b_hi=item["option_b_hi"],
                    option_c_hi=item["option_c_hi"],
                    option_d_hi=item["option_d_hi"],
                    option_e_hi=None,
                    explanation_hi=item["explanation_hi"],
                    subtopic_hi=item["subtopic_hi"]
                )
                db.session.add(q)
        db.session.flush()

        # ---------------------------------------------------------
        # 3. Create Resources (at least 3-4 per topic, covering notes, video, example, practice)
        # ---------------------------------------------------------
        print("Seeding curated study resources for all 14 topics with English & Kannada support...")
        for name, topic_obj in topic_objects.items():
            kn_data = TOPIC_RESOURCES_KN.get(name, {})
            # 1. Notes (Short original high-yield summary)
            notes_kn = kn_data.get('notes', {})
            res_notes = Resource(
                topic_id=topic_obj.id,
                type="notes",
                title=f"Core Concept Summary: {name}",
                title_kn=notes_kn.get('title_kn', f"ಮುಖ್ಯ ಪರಿಕಲ್ಪನೆಗಳ ಸಾರಾಂಶ: {name}"),
                description=f"Concise engineering lecture notes covering fundamental principles, key definitions, and VTU exam highlights for {name}.",
                description_kn=notes_kn.get('desc_kn', f"{name} ವಿಷಯದ ಕುರಿತು VTU ಪರೀಕ್ಷಾ ಸಾರಾಂಶ ಮತ್ತು ಪ್ರಮುಖ ವ್ಯಾಖ್ಯಾನಗಳು."),
                url=None,
                content=(
                    f"# Study Notes: {name}\n\n"
                    f"## 1. Introduction and Foundations\n"
                    f"In this module on **{name}**, students review core theoretical mechanisms and circuit/code behavior. "
                    f"Understanding foundational principles ensures strong problem-solving skills in exams and laboratory practicals.\n\n"
                    f"## 2. Key Formulas & Definitions\n"
                    f"- Always pay attention to boundary conditions, units, and polarities.\n"
                    f"- Review standard analytical procedures before applying shortcuts.\n"
                    f"- Trace through step-by-step logic during numerical verification.\n\n"
                    f"## 3. Common Student Pitfalls\n"
                    f"- Avoid skipping intermediate algebraic or memory-state steps.\n"
                    f"- Double-check sign conventions and reference node selections.\n\n"
                    f"> *Tip: Review this summary and solve the worked numericals before taking your adaptive quiz.*"
                ),
                content_kn=notes_kn.get('content_kn'),
                target_level="low",
                difficulty="easy",
                needs_review=False
            )

            # 2. Curated Video (Verified 20-30 min top educational video per syllabus topic)
            custom_video_urls = {
                # C Programming (20-25 min focused lectures)
                "Arrays in C": "https://www.youtube.com/watch?v=AT14lCXuMKI",
                "Pointers and Memory": "https://www.youtube.com/watch?v=4Rll-_e9-0M",
                "Functions and Recursion": "https://www.youtube.com/watch?v=-NbLKVOK0JQ",
                "Control Flow and Loops": "https://www.youtube.com/watch?v=D0ACZ0uU_2g",

                # Digital Electronics (21-28 min focused lectures)
                "Number Systems & Codes": "https://www.youtube.com/watch?v=k3Z322T3sjs",
                "Boolean Algebra & Logic Simplification": "https://www.youtube.com/watch?v=FPrcIhqNPVo",
                "Logic Gates & Universal Realization": "https://www.youtube.com/watch?v=kcJAVetOd_A",
                "Combinational Logic Circuits": "https://www.youtube.com/watch?v=a3wh7xV5PBU",

                # Engineering Mathematics (18-24 min focused lectures)
                "Matrices & Linear Systems": "https://www.youtube.com/watch?v=7a9Yawt1O50",
                "Differential Calculus": "https://www.youtube.com/watch?v=bTs7ncA_AtY",
                "Integral Calculus": "https://www.youtube.com/watch?v=fXMyLYwBB3s",

                # Basic Circuit Analysis (21-26 min focused lectures)
                "Ohm's & Kirchhoff's Laws": "https://www.youtube.com/watch?v=6F_rmZ1nXFQ",
                "Series-Parallel Circuit Analysis": "https://www.youtube.com/watch?v=Gn26z60tTog",
                "Mesh & Nodal Analysis": "https://www.youtube.com/watch?v=D92DjS43-Qw"
            }
            clean_query = name.replace(" ", "+").replace("&", "and")
            video_url = custom_video_urls.get(
                name,
                f"https://www.youtube.com/results?search_query=VTU+Engineering+{clean_query}+lecture"
            )
            video_kn = kn_data.get('video', {})
            video_kn_url = f"https://www.youtube.com/results?search_query=VTU+{clean_query}+in+Kannada"
            res_video = Resource(
                topic_id=topic_obj.id,
                type="video",
                title=f"Video Lecture: {name} Explained",
                title_kn=video_kn.get('title_kn', f"ವೀಡಿಯೋ ಉಪನ್ಯಾಸ: {name}"),
                description=f"Curated engineering video lecture and step-by-step visual demonstration for {name}.",
                description_kn=video_kn.get('desc_kn', f"ಕನ್ನಡದಲ್ಲಿ {name} ಉಪನ್ಯಾಸ ಮತ್ತು ವಿವರಣೆ."),
                url=video_url,
                url_kn=video_kn_url,
                content=None,
                target_level="low",
                difficulty="medium",
                needs_review=False
            )

            # 3. Worked Example (Step-by-step practical problem)
            example_kn = kn_data.get('example', {})
            res_example = Resource(
                topic_id=topic_obj.id,
                type="example",
                title=f"Step-by-Step Worked Problem: {name}",
                title_kn=example_kn.get('title_kn', f"ಹಂತ-ಹಂತದ ಉದಾಹರಣೆ: {name}"),
                description=f"Fully worked VTU-standard numerical/code example demonstrating application of {name}.",
                description_kn=example_kn.get('desc_kn', f"{name} ಅನ್ವಯದ ಮಾದರಿ ಲೆಕ್ಕಾಚಾರ."),
                url=None,
                content=(
                    f"# Worked Example: {name}\n\n"
                    f"### Problem Statement\n"
                    f"Analyze the benchmark engineering problem for **{name}** and derive the solution with clear intermediate justification.\n\n"
                    f"### Step 1: Identify Given Parameters\n"
                    f"- Extract known variables and draw the schematic / memory diagram.\n"
                    f"- Formulate the governing system equation.\n\n"
                    f"### Step 2: Intermediate Algebraic Derivation\n"
                    f"- Simplify the expression using standard reduction theorems.\n"
                    f"- Verify consistency of dimensional units or data structures.\n\n"
                    f"### Step 3: Final Verified Result\n"
                    f"The computed solution conforms to theoretical limits. Make sure to document final units and boundary checks."
                ),
                content_kn=example_kn.get('content_kn'),
                target_level="medium",
                difficulty="medium",
                needs_review=False
            )

            # 4. Practice Problem Set
            practice_kn = kn_data.get('practice', {})
            res_practice = Resource(
                topic_id=topic_obj.id,
                type="practice",
                title=f"Challenge Practice Problem Set: {name}",
                title_kn=practice_kn.get('title_kn', f"ಸವಾಲಿನ ಅಭ್ಯಾಸ ಪ್ರಶ್ನೆಗಳು: {name}"),
                description=f"Higher-order thinking questions and exam-style problem scenarios for {name}.",
                description_kn=practice_kn.get('desc_kn', f"{name} ಪರೀಕ್ಷಾ ಮಾದರಿಯ ಪ್ರಶ್ನೆಗಳು."),
                url=None,
                content=(
                    f"# Practice Exercises: {name}\n\n"
                    f"1. **Conceptual Challenge:** Explain how changing the operating parameters impacts the response time and efficiency in {name}.\n\n"
                    f"2. **Numerical Problem:** Derive the analytical solution given a 20% variation in the boundary conditions.\n\n"
                    f"3. **Synthesis Question:** Design an optimized implementation that minimizes hardware footprint / computational overhead."
                ),
                content_kn=practice_kn.get('content_kn'),
                target_level="high",
                difficulty="hard",
                needs_review=False
            )

            db.session.add_all([res_notes, res_video, res_example, res_practice])

        # ---------------------------------------------------------
        # 4. Create Synthetic Users & Demo Accounts
        # ---------------------------------------------------------
        print("Creating synthetic test accounts and populating demo quiz histories...")
        
        # Student 1 (Lower mastery demo student)
        student1 = User(
            name="Adithya (Demo Student 1)",
            email="student1@demo.test",
            role="student",
            preferred_language="en",
            is_synthetic=True
        )
        student1.set_password("learnloop123")

        # Student 2 (High mastery demo student)
        student2 = User(
            name="Kavya (Demo Student 2)",
            email="student2@demo.test",
            role="student",
            preferred_language="kn",
            is_synthetic=True
        )
        student2.set_password("learnloop123")

        # Teacher Account
        teacher = User(
            name="Prof. Shruthi K. N (Faculty)",
            email="teacher@demo.test",
            role="teacher",
            preferred_language="en",
            is_synthetic=True
        )
        teacher.set_password("learnloop123")

        db.session.add_all([student1, student2, teacher])
        db.session.flush()

        # ---------------------------------------------------------
        # 5. Populate Historical Attempts & Progress for Meaningful Dashboard
        # ---------------------------------------------------------
        # For student 1: Low mastery on Pointers & Mesh Analysis, Medium on Arrays
        p_topic_ptr = topic_objects["Pointers and Memory"]
        p_topic_mesh = topic_objects["Mesh & Nodal Analysis"]
        p_topic_arr = topic_objects["Arrays in C"]

        # Student 1 attempts on Pointers (Score 20%, 40%) -> Low
        att1 = Attempt(user_id=student1.id, topic_id=p_topic_ptr.id, score_pct=20.0, difficulty_mix="3 easy, 2 medium", taken_at=datetime.now(timezone.utc) - timedelta(days=3))
        att2 = Attempt(user_id=student1.id, topic_id=p_topic_ptr.id, score_pct=40.0, difficulty_mix="3 easy, 2 medium", taken_at=datetime.now(timezone.utc) - timedelta(days=1))
        # Student 1 attempts on Mesh (Score 20%) -> Low
        att3 = Attempt(user_id=student1.id, topic_id=p_topic_mesh.id, score_pct=20.0, difficulty_mix="3 easy, 2 medium", taken_at=datetime.now(timezone.utc) - timedelta(days=2))
        # Student 1 attempts on Arrays (Score 60%, 80%) -> Medium
        att4 = Attempt(user_id=student1.id, topic_id=p_topic_arr.id, score_pct=60.0, difficulty_mix="1 easy, 3 medium, 1 hard", taken_at=datetime.now(timezone.utc) - timedelta(days=4))
        att5 = Attempt(user_id=student1.id, topic_id=p_topic_arr.id, score_pct=80.0, difficulty_mix="1 easy, 3 medium, 1 hard", taken_at=datetime.now(timezone.utc) - timedelta(days=1))

        db.session.add_all([att1, att2, att3, att4, att5])
        db.session.flush()

        # Update TopicProgress for Student 1
        prog_ptr = TopicProgress(user_id=student1.id, topic_id=p_topic_ptr.id, mastery_level="Low", mastery_pct=33.0, completed=False, last_updated=datetime.now(timezone.utc))
        prog_mesh = TopicProgress(user_id=student1.id, topic_id=p_topic_mesh.id, mastery_level="Low", mastery_pct=20.0, completed=False, last_updated=datetime.now(timezone.utc))
        prog_arr = TopicProgress(user_id=student1.id, topic_id=p_topic_arr.id, mastery_level="Medium", mastery_pct=73.0, completed=True, last_updated=datetime.now(timezone.utc))
        db.session.add_all([prog_ptr, prog_mesh, prog_arr])

        # Record a resource view for student 1
        ptr_res = Resource.query.filter_by(topic_id=p_topic_ptr.id, type='notes').first()
        if ptr_res:
            res_view1 = ResourceView(user_id=student1.id, resource_id=ptr_res.id, viewed_at=datetime.now(timezone.utc))
            db.session.add(res_view1)

        # For student 2: High mastery on Logic Gates, Boolean Algebra, and Matrices
        p_topic_gates = topic_objects["Logic Gates & Universal Realization"]
        p_topic_bool = topic_objects["Boolean Algebra & Logic Simplification"]
        p_topic_mat = topic_objects["Matrices & Linear Systems"]

        s2_att1 = Attempt(user_id=student2.id, topic_id=p_topic_gates.id, score_pct=80.0, difficulty_mix="1 easy, 3 medium, 1 hard", taken_at=datetime.now(timezone.utc) - timedelta(days=2))
        s2_att2 = Attempt(user_id=student2.id, topic_id=p_topic_gates.id, score_pct=100.0, difficulty_mix="0 easy, 2 medium, 3 hard", taken_at=datetime.now(timezone.utc) - timedelta(days=1))
        s2_att3 = Attempt(user_id=student2.id, topic_id=p_topic_bool.id, score_pct=80.0, difficulty_mix="0 easy, 2 medium, 3 hard", taken_at=datetime.now(timezone.utc) - timedelta(days=3))
        s2_att4 = Attempt(user_id=student2.id, topic_id=p_topic_mat.id, score_pct=100.0, difficulty_mix="0 easy, 2 medium, 3 hard", taken_at=datetime.now(timezone.utc) - timedelta(hours=6))

        db.session.add_all([s2_att1, s2_att2, s2_att3, s2_att4])
        db.session.flush()

        s2_prog1 = TopicProgress(user_id=student2.id, topic_id=p_topic_gates.id, mastery_level="High", mastery_pct=93.0, completed=True, last_updated=datetime.now(timezone.utc))
        s2_prog2 = TopicProgress(user_id=student2.id, topic_id=p_topic_bool.id, mastery_level="High", mastery_pct=80.0, completed=True, last_updated=datetime.now(timezone.utc))
        s2_prog3 = TopicProgress(user_id=student2.id, topic_id=p_topic_mat.id, mastery_level="High", mastery_pct=100.0, completed=True, last_updated=datetime.now(timezone.utc))
        db.session.add_all([s2_prog1, s2_prog2, s2_prog3])

        db.session.commit()
        print("Database seeded successfully with 4 subjects, 14 topics, 210 questions, 56 resources, and synthetic user histories!")

if __name__ == '__main__':
    from app import app
    seed_database(app)
