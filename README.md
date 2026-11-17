# Learnloop: AI Adaptive Learning Framework for Engineering Students

> *"A personalized, data-driven learning support system designed for engineering students."*

**Institution:** Department of Electronics and Communication Engineering, Government Engineering College, Mosalehosahalli, Hassan (Affiliated to Visvesvaraya Technological University, Belagavi).  
**Academic Context:** Mini Project Synopsis 2026–27  
**Project Team:**
- **Adithya K B** (USN: `4HG24EC002`)
- **Druva** (USN: `4HG24EC016`)
- **G M Kavya** (USN: `4HG24EC017`)
- **Thanusha C P** (USN: `4HG24EC056`)

**Project Guide:** **Prof. Shruthi K. N**, Assistant Professor, Dept. of ECE

---

## 1. Project Overview & Aim

In traditional engineering education, rigid one-size-fits-all curricula often leave student learning gaps unaddressed until high-stakes end-semester examinations. **Learnloop** is a lightweight, low-cost, web-based prototype that closes this loop. By continuously evaluating diagnostic quiz attempts at the topic level, the framework dynamically adjusts question difficulty, identifies learner weaknesses, recommends tailored multi-modal resources (notes, verified video walkthroughs, worked problems, challenge sets), and offers 24/7 multilingual assistance in English, Hindi (हिन्दी), and Kannada (ಕನ್ನಡ).

The core engine operates on **transparent, explainable rule-based logic** (`engine.py`). An optional, disabled-by-default scikit-learn hook (`ml_stub.py`) illustrates where machine learning models can later be validated and integrated without introducing opaque automated grading or vendor lock-in.

---

## 2. Objectives Mapped to Features

| Objective ID | Synopsis Objective | Corresponding Learnloop Feature | Implementation |
| :--- | :--- | :--- | :--- |
| **01** | Student Profile & Progress Logging | Authentication, session state, and attempt persistence | `models.py` (`User`, `Attempt`, `TopicProgress`), `/register`, `/login` |
| **02** | Identify Strengths & Learning Gaps | Three-tier topic mastery bands: Low (&lt;40%), Medium (40–74%), High (≥75%) | `engine.py` (`topic_mastery`, `get_mastery_band`), `/dashboard` |
| **03** | Personalized Multi-Modal Recommendations | Sequence of Notes, Videos, Worked Examples, Practice Sets with clear reasons | `engine.py` (`recommend`), `/quiz/<id>/submit`, `/resources` |
| **04** | Dynamic Difficulty Calibration | Shifts question mix (easy/medium/hard) based on past attempts and score trends | `engine.py` (`next_difficulty`), `/quiz/<id>` |
| **05** | Dual Learner & Teacher Analytics | Chart.js mastery bar & score progression trend lines; read-only class overview | `/dashboard`, `/teacher` (Role-protected) |
| **06** | Multilingual Reviewed AI Chatbot | Real-time Q&A widget in English, हिन्दी, and ಕನ್ನಡ with teacher fallback | `chatbot.py`, `data/chatbot_answers.json`, `/api/chat` |

---

## 3. Directory Layout

```
c:/projects/LearnLoop/
├── app.py                      # Flask factory, session auth, routes, and JSON APIs
├── models.py                   # SQLAlchemy schema (User, Subject, Topic, Question, Attempt, etc.)
├── engine.py                   # Pure-Python rule-based scoring, mastery bands, and recommendation logic
├── ml_stub.py                  # Optional scikit-learn integration hook (disabled by default)
├── chatbot.py                  # Multilingual reviewed-answer engine (EN, HI, KN) with script detection
├── seed.py                     # Database seeder (4 subjects, 14 topics, 168 verified MCQs, resources, synthetic users)
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Dependency specification (Flask, Flask-SQLAlchemy, pytest)
├── data/
│   └── chatbot_answers.json    # Curated multilingual Q&A bank with verified engineering answers
├── templates/
│   ├── base.html               # Shared navbar, glassmorphic header, footer, chatbot drawer partial
│   ├── index.html              # Synopsis-faithful landing page with objectives, team, and references
│   ├── login.html              # Authentication with one-click test demo pills
│   ├── register.html           # Student registration with language preference & privacy notice
│   ├── topics.html             # Syllabus module explorer with mastery badges & quiz triggers
│   ├── quiz.html               # Adaptive quiz taking interface & post-submission recommendation view
│   ├── resources.html          # Searchable, filterable repository of notes, videos, examples, practice
│   ├── resource_detail.html    # In-app viewer for lecture notes and worked numerical solutions
│   ├── teacher.html            # Read-only educator overview: class averages & students needing support
│   └── partials/
│       └── chatbot.html        # Floating chat widget and slide-out multilingual drawer
├── static/
│   ├── style.css               # Design system tokens (Navy, Amber, Teal, Cream) and responsive styles
│   └── script.js               # Client quiz interactivity, Chart.js graphs, and chatbot communication
├── tests/
│   ├── test_engine.py          # Pytest unit tests for engine adaptation logic
│   └── test_chatbot.py         # Pytest unit tests for multilingual chatbot and teacher fallback
└── README.md                   # Complete system documentation
```

---

## 4. Quick Start & Setup Instructions

### Prerequisites
- Python 3.10+ (tested on Python 3.13)
- Modern web browser (Chrome, Edge, Firefox, Safari)
- No Node.js, npm, or paid third-party API keys required.

### Installation Steps

1. **Clone or navigate into the workspace:**
   ```bash
   cd c:/projects/LearnLoop
   ```

2. **Create and activate a virtual environment:**
   - On Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - On Linux / macOS:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the application:**
   ```bash
   python app.py
   ```
   *Note: On first startup, `learnloop.db` is automatically created and seeded with 4 subjects, 14 topics, 168+ technical questions, and demo profiles.*

5. **Open in browser:**
   Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 5. Demo Accounts

The database comes pre-seeded with clearly labeled synthetic test accounts for evaluation:

| Role | Email | Password | Pre-populated Persona / History |
| :--- | :--- | :--- | :--- |
| **Student (Low Mastery)** | `student1@demo.test` | `learnloop123` | Demonstrates learning gaps on *Pointers* (33%) and *Mesh Analysis* (20%); prompts foundational notes-first recommendations. |
| **Student (High Mastery)** | `student2@demo.test` | `learnloop123` | Demonstrates high mastery on *Logic Gates* (93%) and *Matrices* (100%); prompts challenge problems. Preferred language: Kannada. |
| **Faculty / Teacher** | `teacher@demo.test` | `learnloop123` | Accesses the read-only **Teacher Oversight Portal** (`/teacher`) showing class-wide gap detection and low-mastery counts. |

---

## 6. How the Rule-Based Engine Works (`engine.py`)

1. **Scoring Calculation:**
   $$\text{Score} = \left(\frac{\text{Correct Answers}}{\text{Total Questions}}\right) \times 100$$
2. **Weighted Topic Mastery (Recency Prioritization):**
   Mastery considers up to the 3 most recent attempts:
   - 1 Attempt: $100\%$ weight
   - 2 Attempts: $35\%$ on older attempt, $65\%$ on latest attempt
   - 3 Attempts: $20\%$ on oldest, $30\%$ on middle, $50\%$ on latest attempt
3. **Mastery Bands:**
   - **Low Mastery (&lt;40%):** Foundational concepts need reinforcement.
   - **Medium Mastery (40%–74%):** Applied problem solving needed.
   - **High Mastery (≥75%):** Ready for advanced topics and challenge sets.
4. **Adaptive Calibration:**
   - Low Mastery: Quiz served with 3 easy, 2 medium, 0 hard questions.
   - Medium Mastery: Quiz served with 1 easy, 3 medium, 1 hard question.
   - High Mastery: Quiz served with 0 easy, 2 medium, 3 hard questions.
   - Dynamic step-up occurs if student scores $\ge 80\%$; dynamic step-down occurs if student scores $&lt; 40\%$.
5. **Targeted Recommendations:**
   - Low: Notes $\rightarrow$ Video search walkthrough $\rightarrow$ Easy practice set. Reason: *"You scored 20% on Pointers, so we suggest starting with concept notes."*
   - Medium: Worked examples $\rightarrow$ Targeted notes on missed subtopics $\rightarrow$ Intermediate practice.
   - High: Advanced challenge problems $\rightarrow$ Suggestion to advance to the next syllabus module.

---

## 7. Adding Curriculum Topics, Questions, and Chatbot Answers

### Adding a Subject or Topic
Edit `seed.py` or execute via Flask shell:
```python
new_sub = Subject(name="Microcontrollers")
new_topic = Topic(subject_id=new_sub.id, name="8051 Architecture", description="Registers, Timers, and Interrupts.")
db.session.add_all([new_sub, new_topic])
db.session.commit()
```

### Adding MCQs
Add entries to `seed.py` using `add_q(...)`:
```python
add_q(
    t_name="8051 Architecture",
    text="Which register in 8051 holds the program counter after an interrupt?",
    a="DPTR", b="Stack", c="Accumulator", d="B Register",
    correct="B",
    diff="medium",
    subtopic="Interrupt Handling",
    expl="The 8051 pushes the 16-bit PC onto the stack upon interrupt invocation."
)
```

### Adding Reviewed Chatbot Entries
Add a new JSON block to `data/chatbot_answers.json`:
```json
{
  "id": "interrupt_concept",
  "keywords": ["interrupt", "8051", "isr", "इंटरप्ट", "ಇಂಟರಪ್ಟ್"],
  "answer": {
    "en": "An interrupt in microcontrollers temporarily suspends main program execution to service a high-priority event via an ISR.",
    "hi": "माइक्रोकंट्रोलर में इंटरप्ट एक संकेत है जो मुख्य प्रोग्राम को रोककर तत्काल सेवा (ISR) निष्पादित करता है।",
    "kn": "ಮೈಕ್ರೊಕಂಟ್ರೋಲರ್‌ನಲ್ಲಿ ಇಂಟರಪ್ಟ್ ಎನ್ನುವುದು ಮುಖ್ಯ ಪ್ರೋಗ್ರಾಂ ಅನ್ನು ತಾತ್ಕಾಲಿಕವಾಗಿ ನಿಲ್ಲಿಸಿ ಹೆಚ್ಚಿನ ಆದ್ಯತೆಯ ಕಾರ್ಯವನ್ನು ನಿರ್ವಹಿಸುವ ಸಂಕೇತವಾಗಿದೆ."
  }
}
```

---

## 8. Responsible AI Limitations & Safeguards

- **Demonstration Scope:** Demonstrated with a small sample course and synthetic test accounts. Any claim of improved learning outcomes requires formal empirical evaluation.
- **Teacher Primacy:** Learnloop supports teachers and never replaces them. All formal grading, attendance, and evaluation remain exclusively with course faculty.
- **Data Minimization & Privacy:** No sensitive personal identifiers are requested. Passwords are salted and hashed using PBKDF2. Chatbot queries are logged anonymously without user IDs.
- **Explainable Reasoning:** Every recommendation explains why specific materials were prioritized.
- **Hallucination Prevention:** The chatbot answers only from the reviewed bank; unverified questions trigger a courteous redirect to the human teacher.

---

## 9. Future Enhancements

1. **Validated Machine Learning Classifier:** Train a scikit-learn classifier (`ml_stub.py`) to predict multi-week retention risks across entire semester cohorts once sufficient student data is gathered under ethical clearance.
2. **More Languages & Voice Input:** Expand chatbot and lecture note audio synthesis to other regional Indian languages (Telugu, Tamil, Marathi) with regional speech recognition.
3. **Restricted Curriculum LLM:** Deploy a local quantized Language Model (such as Gemma or Llama on an institutional server) strictly constrained to approved VTU engineering textbooks.
4. **LMS Integration:** Support LTI 1.3 / SCORM standards for direct synchronization with VTU institutional Moodle and Canvas platforms.
5. **Empirical Effectiveness Study:** Conduct pre-test/post-test pedagogical evaluations comparing Learnloop adaptive intervention against static lecture delivery.

---

## 10. References

1. M. Murtaza, Y. Ahmed, J. A. Shamsi, F. Sherwani and M. Usman, "AI-Based Personalized E-Learning Systems: Issues, Challenges, and Solutions," *IEEE Access*, vol. 10, pp. 81323-81342, 2022, doi: [10.1109/ACCESS.2022.3193938](https://doi.org/10.1109/ACCESS.2022.3193938).
2. S. G. Essa, T. Celik and N. E. Human-Hendricks, "Personalized Adaptive Learning Technologies Based on Machine Learning Techniques to Identify Learning Styles: A Systematic Literature Review," *IEEE Access*, vol. 11, pp. 48392-48409, 2023, doi: [10.1109/ACCESS.2023.3276439](https://doi.org/10.1109/ACCESS.2023.3276439).
3. G. D. Furman, "Enhancing Engineering Education: The Role of Artificial Intelligence in Personalizing Learning and Outcomes," *2024 4th International Conference on Big Data Engineering and Education (BDEE)*, pp. 61-65, 2024, doi: [10.1109/BDEE63226.2024.00018](https://doi.org/10.1109/BDEE63226.2024.00018).
4. C. Liu, G.-C. Wang and H.-F. Wang, "The Application of Artificial Intelligence in Engineering Education: A Systematic Review," *IEEE Access*, vol. 13, pp. 17895-17910, 2025, doi: [10.1109/ACCESS.2025.3532595](https://doi.org/10.1109/ACCESS.2025.3532595).
5. Official documentation for Python, Flask, SQLite, and scikit-learn.
