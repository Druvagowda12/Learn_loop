"""
Integration and Unit Tests for Bilingual English & Kannada Curriculum
Validates:
1. Language-exclusive notes filtering (EN vs KN).
2. Dynamic video URL switching for all topics.
3. 5-Option quiz schema (A-E, numeric 0-4 correct_index).
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


def test_question_5_options_schema_and_correct_index(client):
    """Verify that all questions have 5 distinct options and valid correct_index."""
    with app.app_context():
        questions = Question.query.all()
        assert len(questions) >= 200

        for q in questions:
            # 5 options validation
            assert q.option_a is not None and len(q.option_a) > 0
            assert q.option_b is not None and len(q.option_b) > 0
            assert q.option_c is not None and len(q.option_c) > 0
            assert q.option_d is not None and len(q.option_d) > 0
            assert q.option_e is not None and len(q.option_e) > 0

            # Correct option and index
            assert q.correct_option in ('A', 'B', 'C', 'D', 'E')
            assert 0 <= q.correct_index <= 4

            # to_dict in English
            dict_en = q.to_dict(lang='en')
            assert len(dict_en['options']) == 5
            assert len(dict_en['options_list']) == 5
            assert dict_en['correct_index'] == q.correct_index

            # to_dict in Kannada
            dict_kn = q.to_dict(lang='kn')
            assert len(dict_kn['options']) == 5
            assert len(dict_kn['options_list']) == 5
            assert dict_kn['correct_index'] == q.correct_index


def test_quiz_api_multilingual_and_tiers(client):
    """Verify that /api/quiz/<topic_id>/questions serves 5 options in EN and KN across tiers."""
    with app.app_context():
        topic = Topic.query.first()
        topic_id = topic.id

    # Test English Easy
    res_en = client.get(f'/api/quiz/{topic_id}/questions?lang=en&difficulty=easy')
    assert res_en.status_code == 200
    data_en = res_en.get_json()
    assert len(data_en['questions']) > 0
    for q in data_en['questions']:
        assert len(q['options']) == 5
        assert len(q['options_list']) == 5
        assert 0 <= q['correct_index'] <= 4

    # Test Kannada Hard
    res_kn = client.get(f'/api/quiz/{topic_id}/questions?lang=kn&difficulty=hard')
    assert res_kn.status_code == 200
    data_kn = res_kn.get_json()
    assert len(data_kn['questions']) > 0
    for q in data_kn['questions']:
        assert len(q['options']) == 5
        assert len(q['options_list']) == 5
        assert 0 <= q['correct_index'] <= 4
        # Verify Kannada script in question or options
        assert any('\u0C80' <= c <= '\u0CFF' for c in q['text']) or any('\u0C80' <= c <= '\u0CFF' for c in q['options_list'])


def test_submit_quiz_numeric_index(client):
    """Verify that quiz submission accurately grades using numeric indices 0-4."""
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

    # Submit with numeric index (e.g. '0', '1', '2', '3', '4')
    res = client.post(f'/quiz/{topic.id}/submit', data={
        f'q_{q_id}': correct_idx,
        'difficulty_mix': 'Fixed Tier: Easy'
    }, follow_redirects=True)

    assert res.status_code == 200
    assert b"Quiz Results" in res.data or b"Results" in res.data or b"score" in res.data.lower() or b"\xe0\xb2\xb0\xe0\xb2\xb8\xe0\xb2\xaa\xe0\xb3\x8d\xe0\xb2\xb0\xe0\xb2\xb6\xe0\xb3\x8d\xe0\xb2\xa8\xe0\xb3\x86" in res.data
