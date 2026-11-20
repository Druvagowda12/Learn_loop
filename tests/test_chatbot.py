"""
Unit tests for Learnloop Multilingual Chatbot (chatbot.py)
"""

import pytest
from chatbot import answer_query, detect_script_language, FALLBACK_MESSAGES, format_api_error_message, load_env_file


def test_script_detection():
    # Latin script defaults to requested
    assert detect_script_language("How does the quiz work?", "en") == "en"
    # Devanagari script triggers Hindi
    assert detect_script_language("क्विज कैसे दें?", "en") == "hi"
    # Kannada script triggers Kannada
    assert detect_script_language("ಕ್ವಿಜ್ ಹೇಗೆ ತೆಗೆದುಕೊಳ್ಳುವುದು?", "en") == "kn"


def test_english_query_matched():
    res = answer_query("How does the quiz work?", requested_lang="en")
    assert res['matched'] is True
    assert res['lang'] == 'en'
    assert "Topics & Quizzes" in res['answer'] or "5" in res['answer']


def test_hindi_query_matched():
    res = answer_query("क्विज के बारे में बताएं", requested_lang="hi")
    assert res['matched'] is True
    assert res['lang'] == 'hi'
    assert "क्विज" in res['answer']


def test_kannada_query_matched():
    res = answer_query("ಕ್ವಿಜ್ ಬಗ್ಗೆ ಮಾಹಿತಿ", requested_lang="kn")
    assert res['matched'] is True
    assert res['lang'] == 'kn'
    assert "ಕ್ವಿಜ್" in res['answer']


def test_concept_pointer_query():
    res = answer_query("What is a pointer in C?", requested_lang="en")
    assert res['matched'] is True
    assert "address" in res['answer'].lower() or "memory" in res['answer'].lower()


def test_unmatched_query_triggers_fallback():
    res = answer_query("What is the stock price of Apple in 2026?", requested_lang="en")
    assert res['matched'] is False
    assert res['lang'] == 'en'
    assert "teacher" in res['answer'].lower() or "instructor" in res['answer'].lower()


def test_unmatched_hindi_fallback():
    res = answer_query("जापान की राजधानी क्या है?", requested_lang="hi")
    assert res['matched'] is False
    assert res['lang'] == 'hi'
    assert "शिक्षक" in res['answer']


def test_format_api_error_message():
    # 400 Invalid key
    msg_400 = format_api_error_message("HTTP 400: API_KEY_INVALID", provider="Google Gemini")
    assert "Invalid API Key" in msg_400
    assert "⚠️" in msg_400

    # 429 Quota
    msg_429 = format_api_error_message("HTTP 429: RESOURCE_EXHAUSTED", provider="Google Gemini")
    assert "Quota Limit Exceeded" in msg_429

    # 404 Deprecated / Not found
    msg_404 = format_api_error_message("HTTP 404: model no longer available", provider="Google Gemini")
    assert "Model Deprecated or Not Found" in msg_404


def test_api_error_returned_to_chat_ui(monkeypatch):
    monkeypatch.setattr('chatbot.call_gemini_api', lambda q, lang, key: (None, "HTTP 404: model deprecated"))
    monkeypatch.setattr('chatbot.get_configured_api_key', lambda passed_key: "test_key_abc")

    res = answer_query("Explain pointers", requested_lang="en")
    assert res['matched'] is False
    assert res['source'] == 'api_error'
    assert "⚠️" in res['answer']
    assert "Model Deprecated or Not Found" in res['answer']

