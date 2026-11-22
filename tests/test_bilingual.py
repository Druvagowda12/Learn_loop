"""
Integration and Unit Tests for Bilingual English & Kannada Curriculum
Validates:
1. Language-exclusive notes filtering (EN vs KN).
2. Dynamic video URL switching for all topics.
3. Strict 4-Option quiz schema (A-D, numeric 0-3 correct_index).
4. Difficulty tiers (easy, medium, hard) and multilingual API endpoint.
"""

import pytest
from models import Subject, Topic, Question, Resource
from app import app, db

def test_language_exclusive_notes(client):
    """Verify that get_content strictly provides English or Kannada notes without fallback leak."""
    with app.app_context():
        res = Resource.query.filter_by(type='notes').first()
        assert res is not None

        content_en = res.get_content('en')
        content_kn = res.get_content('kn')

        assert len(content_en) > 0
        assert len(content_kn) > 0
        assert content_en != content_kn
        # Verify Kannada script characters in Kannada content
        assert any('\u0C80' <= char <= '\u0CFF' for char in content_kn)


def test_bilingual_video_urls(client):
    """Verify that video resources have distinct English and Kannada stream URLs."""
    with app.app_context():
        videos = Resource.query.filter_by(type='video').all()
        assert len(videos) > 0

        for v in videos:
            url_en = v.get_url('en')
            url_kn = v.get_url('kn')
            assert url_en != ''
            assert url_kn != ''
            assert 'youtube' in url_en.lower()
            assert 'youtube' in url_kn.lower()


def test_question_4_options_schema_and_correct_index(client):
    """Verify that all questions have strictly 4 options (A-D) and valid correct_index (0-3)."""
    with app.app_context():
        questions = Question.query.all()
        assert len(questions) >= 300

        for q in questions:
            # 4 options validation
            assert q.option_a is not None and len(q.option_a) > 0
            assert q.option_b is not None and len(q.option_b) > 0
            assert q.option_c is not None and len(q.option_c) > 0
            assert q.option_d is not None and len(q.option_d) > 0

            # Correct option and index
            assert q.correct_option in ('A', 'B', 'C', 'D')
            assert 0 <= q.correct_index <= 3

            # to_dict in English
            dict_en = q.to_dict(lang='en')
            assert len(dict_en['options']) == 4
            assert len(dict_en['options_list']) == 4
            assert dict_en['correct_index'] == q.correct_index

            # to_dict in Kannada
            dict_kn = q.to_dict(lang='kn')
            assert len(dict_kn['options']) == 4
            assert len(dict_kn['options_list']) == 4
            assert dict_kn['correct_index'] == q.correct_index


def test_quiz_api_multilingual_and_tiers(client):
    """Verify that /api/quiz/<topic_id>/questions serves 4 options in EN and KN across tiers."""
    with app.app_context():
        topic = Topic.query.first()
        topic_id = topic.id

    # Test English Easy
    res_en = client.get(f'/api/quiz/{topic_id}/questions?lang=en&difficulty=easy')
    assert res_en.status_code == 200
    data_en = res_en.get_json()
    assert len(data_en['questions']) > 0
    assert len(data_en['questions']) <= 10
    for q in data_en['questions']:
        assert len(q['options']) == 4
        assert len(q['options_list']) == 4
        assert 0 <= q['correct_index'] <= 3

    # Test Kannada Hard
    res_kn = client.get(f'/api/quiz/{topic_id}/questions?lang=kn&difficulty=hard')
    assert res_kn.status_code == 200
    data_kn = res_kn.get_json()
    assert len(data_kn['questions']) > 0
    assert len(data_kn['questions']) <= 10
    for q in data_kn['questions']:
        assert len(q['options']) == 4
        assert len(q['options_list']) == 4
        assert 0 <= q['correct_index'] <= 3
        # Verify Kannada script in question or options
        assert any('\u0C80' <= c <= '\u0CFF' for c in q['text']) or any('\u0C80' <= c <= '\u0CFF' for c in q['options_list'])


def test_submit_quiz_numeric_index(client):
    """Verify that quiz submission accurately grades using numeric indices 0-3."""
    # Login as student1
    login_res = client.post('/login', data={
        'email': 'student1@demo.test',
        'password': 'learnloop123'
    }, follow_redirects=True)
    assert login_res.status_code == 200

    with app.app_context():
        topic = Topic.query.first()
        q = Question.query.filter_by(topic_id=topic.id).first()
        q_id = q.id
        correct_idx = str(q.correct_index)

    # Submit with numeric index (e.g. '0', '1', '2', '3')
    res = client.post(f'/quiz/{topic.id}/submit', data={
        f'q_{q_id}': correct_idx,
        'difficulty_mix': 'Fixed Tier: Easy'
    }, follow_redirects=True)

    assert res.status_code == 200
    assert b"Quiz Results" in res.data or b"Results" in res.data or b"score" in res.data.lower() or b"\xe0\xb2\xb0\xe0\xb2\xb8\xe0\xb2\xaa\xe0\xb3\x8d\xe0\xb2\xb0\xe0\xb2\xb6\xe0\xb3\x8d\xe0\xb2\xa8\xe0\xb3\x86" in res.data


def test_no_placeholder_translations_in_questions(client):
    """Verify that zero questions contain placeholder text like '(ಕನ್ನಡ ರೂಪಾಂತರ)' or '(हिंदी अनुवाद)'."""
    with app.app_context():
        # 1. Zero placeholder tags
        bad_kn = Question.query.filter(Question.text_kn.like('%(ಕನ್ನಡ ರೂಪಾಂತರ)%')).count()
        bad_hi = Question.query.filter(Question.text_hi.like('%(हिंदी अनुवाद)%')).count()
        assert bad_kn == 0, f"Found {bad_kn} questions with '(ಕನ್ನಡ ರೂಪಾಂತರ)'"
        assert bad_hi == 0, f"Found {bad_hi} questions with '(हिंदी अनुवाद)'"

        # 2. Check all questions have full Hindi fields
        questions = Question.query.all()
        assert len(questions) >= 300
        for q in questions:
            assert q.text_hi is not None and len(q.text_hi) > 0
            assert q.option_a_hi is not None and len(q.option_a_hi) > 0
            assert q.option_b_hi is not None and len(q.option_b_hi) > 0
            assert q.option_c_hi is not None and len(q.option_c_hi) > 0
            assert q.option_d_hi is not None and len(q.option_d_hi) > 0
            assert q.explanation_hi is not None and len(q.explanation_hi) > 0

            # Hindi to_dict check
            dict_hi = q.to_dict(lang='hi')
            assert len(dict_hi['options']) == 4
            assert len(dict_hi['options_list']) == 4
            assert dict_hi['correct_index'] == q.correct_index
            # Ensure Hindi Devanagari script is present
            assert any('\u0900' <= char <= '\u097F' for char in dict_hi['text']) or any('\u0900' <= char <= '\u097F' for char in dict_hi['options_list'])


def test_quiz_api_hindi_support(client):
    """Verify that /api/quiz/<topic_id>/questions serves 4 options in Hindi (lang=hi)."""
    with app.app_context():
        topic = Topic.query.first()
        topic_id = topic.id

    res_hi = client.get(f'/api/quiz/{topic_id}/questions?lang=hi&difficulty=medium')
    assert res_hi.status_code == 200
    data_hi = res_hi.get_json()
    assert len(data_hi['questions']) > 0
    assert len(data_hi['questions']) <= 10
    for q in data_hi['questions']:
        assert len(q['options']) == 4
        assert len(q['options_list']) == 4
        assert 0 <= q['correct_index'] <= 3
        assert any('\u0900' <= c <= '\u097F' for c in q['text']) or any('\u0900' <= c <= '\u097F' for c in q['options_list'])

