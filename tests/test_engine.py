"""
Unit tests for Learnloop Adaptation Engine (engine.py)
"""

import pytest
from engine import (
    compute_attempt_score,
    get_mastery_band,
    topic_mastery,
    next_difficulty,
    recommend,
    MIX_EASY_HEAVY,
    MIX_BALANCED,
    MIX_HARD_HEAVY
)


def test_compute_attempt_score_empty():
    assert compute_attempt_score([]) == 0.0


def test_compute_attempt_score_all_correct():
    results = [{'is_correct': True}] * 5
    assert compute_attempt_score(results) == 100.0


def test_compute_attempt_score_partial():
    results = [
        {'is_correct': True},
        {'is_correct': False},
        {'is_correct': True},
        {'is_correct': False},
        {'is_correct': False}
    ]
    # 2 out of 5 = 40.0%
    assert compute_attempt_score(results) == 40.0


def test_mastery_band_thresholds():
    assert get_mastery_band(0.0) == 'Low'
    assert get_mastery_band(39.9) == 'Low'
    assert get_mastery_band(40.0) == 'Medium'
    assert get_mastery_band(74.9) == 'Medium'
    assert get_mastery_band(75.0) == 'High'
    assert get_mastery_band(100.0) == 'High'


def test_topic_mastery_single_attempt():
    res = topic_mastery([{'score_pct': 60.0}])
    assert res['mastery_pct'] == 60.0
    assert res['mastery_level'] == 'Medium'
    assert res['attempts_count'] == 1


def test_topic_mastery_two_attempts_recency_weighting():
    # 2 attempts: 0.35 * 40 + 0.65 * 80 = 14 + 52 = 66.0
    res = topic_mastery([{'score_pct': 40.0}, {'score_pct': 80.0}])
    assert res['mastery_pct'] == 66.0
    assert res['mastery_level'] == 'Medium'


def test_topic_mastery_three_attempts_recency_weighting():
    # 3 attempts: 0.20 * 20 + 0.30 * 60 + 0.50 * 80 = 4 + 18 + 40 = 62.0
    res = topic_mastery([{'score_pct': 20.0}, {'score_pct': 60.0}, {'score_pct': 80.0}])
    assert res['mastery_pct'] == 62.0
    assert res['mastery_level'] == 'Medium'


def test_next_difficulty_low_mastery():
    diff = next_difficulty('Low', last_score=20.0)
    assert diff == MIX_EASY_HEAVY


def test_next_difficulty_step_up_on_high_score():
    # Even if Medium, a score of 80% should step difficulty up to hard-heavy
    diff = next_difficulty('Medium', last_score=80.0)
    assert diff == MIX_HARD_HEAVY


def test_next_difficulty_step_down_on_low_score():
    # High mastery student scoring < 40% drops back to easy-heavy
    diff = next_difficulty('High', last_score=20.0)
    assert diff == MIX_EASY_HEAVY


def test_recommendation_low_mastery():
    rec = recommend("Pointers", "Low", 20.0, missed_subtopics=["Address Operator"])
    assert rec['mastery_level'] == 'Low'
    assert rec['recommended_sequence'][0] == 'notes'
    assert 'Address Operator' in rec['reason']
    assert 'Pointers' in rec['reason']


def test_recommendation_high_mastery():
    rec = recommend("Matrices", "High", 100.0)
    assert rec['mastery_level'] == 'High'
    assert rec['recommended_sequence'][0] == 'practice'
    assert 'advanced' in rec['reason'].lower() or 'congratulations' in rec['reason'].lower()
