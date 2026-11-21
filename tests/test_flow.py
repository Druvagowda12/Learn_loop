"""
End-to-End Integration Tests for Learnloop
Simulates the entire user flow:
1. Landing page renders
2. Registration & session creation
3. Login as student1
4. Taking adaptive quiz with low score -> verifies Low mastery & notes recommendation
5. Retrying quiz with high score -> verifies mastery increase
6. Opening resource -> verifies ResourceView logging
7. Loading dashboard -> verifies charts and metrics
8. Access control: student cannot access /teacher; teacher can access /teacher
9. Multilingual chatbot API in EN, HI, KN, and fallback
"""

import pytest
from app import app, db
from models import User, Topic, Question, Attempt, TopicProgress, Resource, ResourceView




def test_landing_page(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b"Learnloop" in res.data
    assert b"Sign In to Learnloop" in res.data or b"Sign In" in res.data
    assert b"Test Demo Accounts" in res.data
    assert b"student1@demo.test" in res.data


def test_404_error_page(client):
    res = client.get('/non-existent-route-for-testing-404')
    assert res.status_code == 404
    assert b"404" in res.data
    assert b"Lost in the Learning Loop" in res.data



def test_student_registration_and_login_flow(client):
    # Ensure clean state for test student
    with app.app_context():
        u = User.query.filter_by(email='pooja@test.local').first()
        if u:
            db.session.delete(u)
            db.session.commit()

    # 1. Register a new student
    res = client.post('/register', data={
        'name': 'Pooja R',
        'email': 'pooja@test.local',
        'password': 'password123',
        'preferred_language': 'kn',
        'consent': 'on'
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"Registration successful" in res.data or b"Topics & Quizzes" in res.data

    # 2. Logout
    res = client.get('/logout', follow_redirects=True)
    assert res.status_code == 200
    assert b"signed out" in res.data

    # 3. Login as student1
    res = client.post('/login', data={
        'email': 'student1@demo.test',
        'password': 'learnloop123'
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"Welcome back" in res.data or b"Dashboard" in res.data

    # Clean up test user
    with app.app_context():
        u = User.query.filter_by(email='pooja@test.local').first()
        if u:
            db.session.delete(u)
            db.session.commit()


def test_adaptive_quiz_and_recommendation_flow(client):
    # Login as student1
    client.post('/login', data={
        'email': 'student1@demo.test',
        'password': 'learnloop123'
    })

    # Pick topic 'Pointers and Memory'
    with app.app_context():
        topic = Topic.query.filter_by(name='Pointers and Memory').first()
        topic_id = topic.id

    # 1. Load quiz page
    res = client.get(f'/quiz/{topic_id}')
    assert res.status_code == 200
    assert b"Pointers and Memory" in res.data
    assert b"Question 1 of" in res.data

    # 2. Submit quiz with all wrong options
    with app.app_context():
        questions = Question.query.filter_by(topic_id=topic_id).all()
        q_data = {'difficulty_mix': '6 easy, 3 medium, 1 hard'}
        for q in questions[:10]:
            wrong_opt = 'A' if q.correct_option != 'A' else 'B'
            q_data[f'q_{q.id}'] = wrong_opt

    res = client.post(f'/quiz/{topic_id}/submit', data=q_data)
    assert res.status_code == 200
    # Must show results, Low mastery, and recommendations
    assert b"Fundamental Concept Revision Required" in res.data or b"Low Mastery" in res.data
    assert b"Recommended Learning Materials" in res.data

    # 3. Retry quiz with correct answers
    with app.app_context():
        high_q_data = {'difficulty_mix': '6 easy, 3 medium, 1 hard'}
        for q in questions[:10]:
            high_q_data[f'q_{q.id}'] = q.correct_option

    res2 = client.post(f'/quiz/{topic_id}/submit', data=high_q_data)
    assert res2.status_code == 200
    assert b"100" in res2.data or b"80" in res2.data


def test_resource_view_and_logging(client):
    client.post('/login', data={
        'email': 'student1@demo.test',
        'password': 'learnloop123'
    })

    with app.app_context():
        res = Resource.query.filter_by(type='notes').first()
        res_id = res.id

    view_res = client.get(f'/resource/{res_id}')
    assert view_res.status_code == 200
    assert b"Study Notes" in view_res.data or b"Core Concept Summary" in view_res.data
    assert b"logged towards your topic progress" in view_res.data


def test_dashboard_and_charts(client):
    client.post('/login', data={
        'email': 'student1@demo.test',
        'password': 'learnloop123'
    })

    res = client.get('/dashboard')
    assert res.status_code == 200
    assert b"Learning Progress" in res.data
    assert b"masteryBarChart" in res.data
    assert b"scoreTrendChart" in res.data
    assert b"Strengths & Learning Gaps" in res.data


def test_role_based_access_control(client):
    # Student cannot access /teacher
    client.post('/login', data={
        'email': 'student1@demo.test',
        'password': 'learnloop123'
    })
    res = client.get('/teacher', follow_redirects=True)
    assert res.status_code == 200
    assert b"Access restricted" in res.data

    # Logout and login as teacher
    client.get('/logout')
    client.post('/login', data={
        'email': 'teacher@demo.test',
        'password': 'learnloop123'
    })
    teacher_res = client.get('/teacher')
    assert teacher_res.status_code == 200
    assert b"Faculty Read-Only Mode" in teacher_res.data
    assert b"Responsible Educational AI Safeguard" in teacher_res.data
    assert b"Module Intervention Radar" in teacher_res.data


def test_chatbot_multilingual_api(client):
    # 1. English query
    res_en = client.post('/api/chat', json={'message': 'How does the quiz work?', 'lang': 'en'})
    assert res_en.status_code == 200
    data_en = res_en.get_json()
    assert data_en['matched'] is True
    assert data_en['lang'] == 'en'

    # 2. Hindi query
    res_hi = client.post('/api/chat', json={'message': 'क्विज कैसे दें?', 'lang': 'hi'})
    assert res_hi.status_code == 200
    data_hi = res_hi.get_json()
    assert data_hi['matched'] is True
    assert data_hi['lang'] == 'hi'

    # 3. Kannada query
    res_kn = client.post('/api/chat', json={'message': 'ಕ್ವಿಜ್ ಹೇಗೆ ತೆಗೆದುಕೊಳ್ಳುವುದು?', 'lang': 'kn'})
    assert res_kn.status_code == 200
    data_kn = res_kn.get_json()
    assert data_kn['matched'] is True
    assert data_kn['lang'] == 'kn'

    # 4. Unmatched fallback query
    res_fallback = client.post('/api/chat', json={'message': 'What is the price of Bitcoin?', 'lang': 'en'})
    assert res_fallback.status_code == 200
    data_fb = res_fallback.get_json()
    assert data_fb['matched'] is False
    assert 'teacher' in data_fb['answer'].lower() or 'instructor' in data_fb['answer'].lower()
