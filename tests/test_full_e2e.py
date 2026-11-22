"""
End-to-End DevSecOps & QA Automated Test Suite for LearnLoop
============================================================
Covers:
1. Public & Core Endpoints (Home, Topics, Repository, Favicon, Chatbot)
2. Authentication & RBAC (Student & Faculty Registration, Access Code Verification, Login/Logout)
3. Role-Based Access Control (Student denied /faculty -> redirected; Faculty allowed)
4. Trilingual Adaptive Quiz Flow (EN, KN, HI 4-options, submission, persistence to quiz_attempts, GET redirect)
5. Edge Cases (Empty inputs, duplicate email, missing consent, invalid IDs, method handling)
"""

import os
import json
import pytest
from app import app, db
from models import User, Topic, Question, Attempt, QuizAttempt, Resource


def test_public_and_core_endpoints(client):
    """Verify core public endpoints render cleanly with 200 OK."""
    # Home landing page
    res_home = client.get('/')
    assert res_home.status_code == 200
    assert b"Learnloop" in res_home.data

    # Topics catalog
    res_topics = client.get('/topics')
    assert res_topics.status_code == 200
    assert b"C Programming" in res_topics.data or b"Digital Electronics" in res_topics.data

    # Repository / Resources
    res_res = client.get('/resources')
    assert res_res.status_code == 200

    # Favicon route (prevent 404 asset noise)
    res_fav = client.get('/favicon.ico')
    assert res_fav.status_code == 200
    assert b"svg" in res_fav.data or res_fav.content_type.startswith("image/")

    # Chatbot API GET status check
    res_chat_get = client.get('/api/chat')
    assert res_chat_get.status_code == 200
    data_chat_get = res_chat_get.get_json()
    assert data_chat_get.get('status') == 'active'

    # Chatbot API query in English
    res_chat_en = client.post('/api/chat', json={'message': 'What is KVL?', 'lang': 'en'})
    assert res_chat_en.status_code == 200
    assert 'answer' in res_chat_en.get_json()

    # Chatbot API query in Kannada
    res_chat_kn = client.post('/api/chat', json={'message': 'ಕಲನಶಾಸ್ತ್ರ ಎಂದರೇನು?', 'lang': 'kn'})
    assert res_chat_kn.status_code == 200
    assert 'answer' in res_chat_kn.get_json()

    # Chatbot API query in Hindi
    res_chat_hi = client.post('/api/chat', json={'message': 'कलन क्या है?', 'lang': 'hi'})
    assert res_chat_hi.status_code == 200
    assert 'answer' in res_chat_hi.get_json()


def test_student_and_faculty_registration_and_auth(client):
    """Test full registration, faculty access code verification, and login/logout."""
    # 1. Successful Student Registration
    res_reg_student = client.post('/register', data={
        'name': 'Aarav Sharma',
        'email': 'aarav.sharma@example.edu',
        'password': 'Password123!',
        'role': 'student',
        'preferred_language': 'en',
        'consent': 'on'
    }, follow_redirects=True)
    assert res_reg_student.status_code == 200
    with client.session_transaction() as sess:
        assert sess.get('role') == 'student'
        assert sess.get('user_name') == 'Aarav Sharma'

    # Logout
    res_logout = client.get('/logout', follow_redirects=True)
    assert res_logout.status_code == 200
    with client.session_transaction() as sess:
        assert 'user_id' not in sess

    # Student Login
    res_login = client.post('/login', data={
        'email': 'aarav.sharma@example.edu',
        'password': 'Password123!'
    }, follow_redirects=True)
    assert res_login.status_code == 200
    with client.session_transaction() as sess:
        assert sess.get('role') == 'student'

    client.get('/logout')

    # 2. Faculty Registration with WRONG Access Code -> 403 Forbidden
    res_faculty_fail = client.post('/register', data={
        'name': 'Prof. Ramanujan',
        'email': 'prof.ramanujan@example.edu',
        'password': 'FacultyPassword123!',
        'role': 'faculty',
        'faculty_access_code': 'WRONG_CODE_999',
        'preferred_language': 'en',
        'consent': 'on'
    })
    assert res_faculty_fail.status_code == 403
    assert b"Invalid Faculty Access Code" in res_faculty_fail.data

    # 3. Faculty Registration with CORRECT Access Code -> Success & Redirect to Faculty Portal
    expected_code = os.getenv('FACULTY_ACCESS_CODE', 'GECM@123').strip().strip('"').strip("'")
    res_faculty_ok = client.post('/register', data={
        'name': 'Prof. Ramanujan',
        'email': 'prof.ramanujan@example.edu',
        'password': 'FacultyPassword123!',
        'role': 'faculty',
        'faculty_access_code': expected_code,
        'preferred_language': 'en',
        'consent': 'on'
    }, follow_redirects=True)
    assert res_faculty_ok.status_code == 200
    assert b"Faculty Oversight Portal" in res_faculty_ok.data or b"Module Intervention Radar" in res_faculty_ok.data
    with client.session_transaction() as sess:
        assert sess.get('role') == 'faculty'


def test_rbac_access_control(client):
    """Test Role-Based Access Control on faculty routes."""
    # 1. Unauthenticated request to /faculty -> returns 403 Forbidden
    res_unauth_fac = client.get('/faculty')
    assert res_unauth_fac.status_code == 403

    # Unauthenticated request to /teacher -> redirects to /login
    res_unauth_teach = client.get('/teacher', follow_redirects=False)
    assert res_unauth_teach.status_code == 302
    assert '/login' in res_unauth_teach.headers.get('Location', '')

    # 2. Student logged in -> access to /faculty returns 403 Forbidden
    client.post('/login', data={
        'email': 'student1@demo.test',
        'password': 'learnloop123'
    })
    res_student_faculty = client.get('/faculty')
    assert res_student_faculty.status_code == 403

    # Student accessing /teacher redirects to /dashboard
    res_student_teacher = client.get('/teacher', follow_redirects=False)
    assert res_student_teacher.status_code == 302
    assert '/dashboard' in res_student_teacher.headers.get('Location', '')

    client.get('/logout')

    # 3. Faculty logged in -> access to /faculty and /teacher allowed (200 OK)
    client.post('/login', data={
        'email': 'teacher@demo.test',
        'password': 'learnloop123'
    })
    res_faculty = client.get('/faculty')
    assert res_faculty.status_code == 200
    assert b"Faculty Oversight Portal" in res_faculty.data or b"Intervention Radar" in res_faculty.data

    res_teacher = client.get('/teacher')
    assert res_teacher.status_code == 200


def test_trilingual_quiz_flow_and_persistence(client):
    """Test 4-option questions in en/kn/hi, quiz submission, persistence to quiz_attempts, and GET redirect."""
    client.post('/login', data={
        'email': 'student1@demo.test',
        'password': 'learnloop123'
    })

    # Test question API in English, Kannada, and Hindi
    for lang in ['en', 'kn', 'hi']:
        res_q = client.get(f'/api/quiz/1/questions?lang={lang}')
        assert res_q.status_code == 200
        data = res_q.get_json()
        assert 'questions' in data
        assert len(data['questions']) == 10
        for q in data['questions']:
            # Strictly 4 options
            assert 'options' in q
            assert set(q['options'].keys()) == {'A', 'B', 'C', 'D'}
            assert 'E' not in q['options']

    # Submit Quiz via POST
    with app.app_context():
        questions = Question.query.filter_by(topic_id=1).all()
        sub_data = {'difficulty_mix': '4 easy, 4 medium, 2 hard'}
        for q in questions[:10]:
            sub_data[f'q_{q.id}'] = q.correct_option

    res_submit = client.post('/quiz/1/submit', data=sub_data)
    assert res_submit.status_code == 200
    assert b"Quiz Complete" in res_submit.data or b"Results" in res_submit.data or b"Performance Summary" in res_submit.data

    # Verify record was stored in Neon / SQLAlchemy QuizAttempt table
    with app.app_context():
        u = User.query.filter_by(email='student1@demo.test').first()
        qa = QuizAttempt.query.filter_by(user_id=u.id).order_by(QuizAttempt.id.desc()).first()
        assert qa is not None
        assert qa.topic is not None
        assert qa.score_percent is not None
        assert qa.difficulty == '4 easy, 4 medium, 2 hard'

    # Refreshing or directly navigating via GET to /quiz/1/submit safely redirects to /quiz/1
    res_get_submit = client.get('/quiz/1/submit', follow_redirects=False)
    assert res_get_submit.status_code == 302
    assert '/quiz/1' in res_get_submit.headers.get('Location', '')


def test_edge_cases_and_error_handling(client):
    """Test empty forms, missing consent, duplicate emails, invalid IDs, and invalid method handling."""
    # 1. Empty registration inputs
    res_empty = client.post('/register', data={
        'name': '',
        'email': '',
        'password': '',
        'consent': 'on'
    })
    assert res_empty.status_code == 200
    assert b"Please fill in all required fields" in res_empty.data

    # 2. Missing consent checkbox
    res_no_consent = client.post('/register', data={
        'name': 'Test User',
        'email': 'noconsent@example.com',
        'password': 'ValidPassword123!',
        'consent': ''
    })
    assert res_no_consent.status_code == 200
    assert b"academic data consent" in res_no_consent.data

    # 3. Duplicate email registration redirects to login
    res_dup = client.post('/register', data={
        'name': 'Duplicate User',
        'email': 'student1@demo.test',
        'password': 'ValidPassword123!',
        'consent': 'on'
    }, follow_redirects=False)
    assert res_dup.status_code == 302
    assert '/login' in res_dup.headers.get('Location', '')

    # 4. Non-existent topic returns clean 404
    client.post('/login', data={'email': 'student1@demo.test', 'password': 'learnloop123'})
    res_404_quiz = client.get('/quiz/999999')
    assert res_404_quiz.status_code == 404
    assert b"404" in res_404_quiz.data

    # 5. Non-existent resource returns clean 404
    res_404_res = client.get('/resource/999999')
    assert res_404_res.status_code == 404

    # 6. GET on /api/set-api-key returns JSON status (no 405 error)
    res_key_get = client.get('/api/set-api-key')
    assert res_key_get.status_code == 200
    assert 'has_key' in res_key_get.get_json()

    # 7. GET on /faculty/clear-student-data safely redirects (no 405 error)
    client.post('/login', data={'email': 'teacher@demo.test', 'password': 'learnloop123'})
    res_clear_get = client.get('/faculty/clear-student-data', follow_redirects=False)
    assert res_clear_get.status_code == 302


def test_faculty_student_data_management_reset_and_remove(client):
    """Test explicit child record deletion, foreign key safety, and rollback handling for reset_student and delete_student."""
    from models import AttemptAnswer, TopicProgress, ResourceView, LessonProgress, Certificate

    # 1. Ensure test student 'leo' exists with active attempts and progress
    with app.app_context():
        student = User.query.filter_by(email='leo@student.test').first()
        if not student:
            student = User(
                name='Leo Test',
                email='leo@student.test',
                role='student',
                preferred_language='en'
            )
            student.set_password('password123')
            db.session.add(student)
            db.session.commit()

        student_id = student.id

        # Add sample attempt and answer
        att = Attempt(user_id=student_id, topic_id=1, score_pct=80.0, difficulty_mix='adaptive')
        db.session.add(att)
        db.session.commit()

        q = Question.query.filter_by(topic_id=1).first()
        if q:
            ans = AttemptAnswer(attempt_id=att.id, question_id=q.id, chosen_option='A', is_correct=True)
            db.session.add(ans)

        # Add QuizAttempt, LessonProgress, and TopicProgress
        qa = QuizAttempt(user_id=student_id, subject='C Programming', topic='Functions', difficulty='medium', score_percent=80.0)
        db.session.add(qa)

        tp = TopicProgress(user_id=student_id, topic_id=1, mastery_level='Medium', mastery_pct=80.0)
        db.session.add(tp)

        db.session.commit()

    # 2. Log in as faculty
    client.post('/login', data={'email': 'teacher@demo.test', 'password': 'learnloop123'})

    # 3. Trigger Reset Data for student
    res_reset = client.post('/faculty/clear-student-data', data={
        'action': 'reset_student',
        'student_id': student_id
    }, follow_redirects=True)
    assert res_reset.status_code == 200
    assert b"reset to zero successfully" in res_reset.data or b"records for student" in res_reset.data

    with app.app_context():
        # User still exists, but all attempt/progress records are wiped clean
        u = db.session.get(User, student_id)
        assert u is not None
        assert Attempt.query.filter_by(user_id=student_id).count() == 0
        assert QuizAttempt.query.filter_by(user_id=student_id).count() == 0
        assert TopicProgress.query.filter_by(user_id=student_id).count() == 0

    # 4. Trigger Remove Student
    res_delete = client.post('/faculty/clear-student-data', data={
        'action': 'delete_student',
        'student_id': student_id
    }, follow_redirects=True)
    assert res_delete.status_code == 200
    assert b"removed successfully" in res_delete.data

    with app.app_context():
        assert db.session.get(User, student_id) is None


def test_trilingual_study_notes_reader(client):
    """Verify that resource study notes render cleanly across EN, KN, and HI."""
    with app.app_context():
        note = Resource.query.filter_by(type='notes').first()
        assert note is not None
        note_id = note.id

    # Test English
    res_en = client.get(f'/resource/{note_id}?lang=en')
    assert res_en.status_code == 200
    assert b"English Version Active" in res_en.data or b"English" in res_en.data
    assert b"study-notes-body" in res_en.data

    # Test Kannada
    res_kn = client.get(f'/resource/{note_id}?lang=kn')
    assert res_kn.status_code == 200
    assert b"study-notes-body" in res_kn.data

    # Test Hindi
    res_hi = client.get(f'/resource/{note_id}?lang=hi')
    assert res_hi.status_code == 200
    assert b"study-notes-body" in res_hi.data


def test_faculty_study_notes_crud(client):
    """Verify that faculty can edit existing study notes and create new ones, while students are blocked."""
    with app.app_context():
        note = Resource.query.filter_by(type='notes').first()
        assert note is not None
        note_id = note.id

    # 1. Unauthenticated or student access should be blocked (403)
    res_blocked = client.get(f'/faculty/notes/edit/{note_id}')
    assert res_blocked.status_code == 403

    # Student logged in
    client.post('/login', data={'email': 'student@demo.test', 'password': 'learnloop123'})
    res_student_blocked = client.get(f'/faculty/notes/edit/{note_id}')
    assert res_student_blocked.status_code == 403
    client.get('/logout')

    # 2. Faculty logged in can access editor
    client.post('/login', data={'email': 'teacher@demo.test', 'password': 'learnloop123'})
    res_faculty_get = client.get(f'/faculty/notes/edit/{note_id}')
    assert res_faculty_get.status_code == 200
    assert b"Edit Notes" in res_faculty_get.data

    # 3. Faculty POST edit
    res_faculty_post = client.post(f'/faculty/notes/edit/{note_id}', data={
        'difficulty': 'hard',
        'target_level': 'high',
        'title': 'Updated Comprehensive Study Notes',
        'title_kn': 'ನವೀಕರಿಸಿದ ಸಮಗ್ರ ಟಿಪ್ಪಣಿಗಳು',
        'title_hi': 'अद्यतनित व्यापक अध्ययन नोट्स',
        'description': 'Updated description for testing.',
        'description_kn': 'ಕನ್ನಡ ವಿವರಣೆ',
        'description_hi': 'हिन्दी विवरण',
        'content': '### 1. Detailed Concept Explanation\nUpdated content text for test.',
        'content_kn': '### 1. ವಿವರವಾದ ಪರಿಕಲ್ಪನೆ ವಿವರಣೆ\nಕನ್ನಡ ಪಠ್ಯ.',
        'content_hi': '### 1. विस्तृत अवधारणा व्याख्या\nहिन्दी पाठ।'
    }, follow_redirects=True)
    assert res_faculty_post.status_code == 200
    assert b"updated successfully" in res_faculty_post.data

    with app.app_context():
        updated_note = db.session.get(Resource, note_id)
        assert updated_note.title == 'Updated Comprehensive Study Notes'
        assert updated_note.difficulty == 'hard'

    # 4. Faculty create new note
    res_create_get = client.get('/faculty/notes/create')
    assert res_create_get.status_code == 200

    res_create_post = client.post('/faculty/notes/create', data={
        'topic_id': 1,
        'difficulty': 'medium',
        'target_level': 'medium',
        'title': 'New Test Study Note',
        'title_kn': 'ಹೊಸ ಟಿಪ್ಪಣಿ',
        'title_hi': 'नया नोट',
        'content': 'Test content in English',
        'content_kn': 'ಕನ್ನಡ ಪಠ್ಯ',
        'content_hi': 'हिन्दी पाठ'
    }, follow_redirects=True)
    assert res_create_post.status_code == 200

    with app.app_context():
        created = Resource.query.filter_by(title='New Test Study Note').first()
        assert created is not None
        assert created.topic_id == 1

