"""
Learnloop Flask Application
===========================
AI Adaptive Learning Framework for Engineering Students.
College Mini Project (VTU Belagavi, 2026-27).
"""

import os
import random
import json
import sys
import socket
import urllib.request
from datetime import datetime, timezone
from functools import wraps

# Campus/LAN DNS fallback resolver for Neon cloud connections
_orig_getaddrinfo = socket.getaddrinfo
def _safe_neon_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    try:
        return _orig_getaddrinfo(host, port, family, type, proto, flags)
    except socket.gaierror:
        if 'neon.tech' in host:
            try:
                url = f"https://dns.google/resolve?name={host}&type=A"
                req = urllib.request.urlopen(url, timeout=3)
                data = json.loads(req.read().decode())
                ips = [a['data'] for a in data.get('Answer', []) if a.get('type') == 1]
                if ips:
                    p = int(port or 5432)
                    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (ip, p)) for ip in ips]
            except Exception:
                pass
        raise
socket.getaddrinfo = _safe_neon_getaddrinfo

from dotenv import load_dotenv
load_dotenv()  # Load variables from .env into os.environ (no-op if file absent)

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, jsonify, abort, g
)

from models import (
    db, User, Subject, Topic, Question,
    Attempt, AttemptAnswer, TopicProgress,
    Resource, ResourceView, ChatLog, utc_now
)

from engine import (
    compute_attempt_score, topic_mastery,
    next_difficulty, recommend, get_mastery_band
)

from chatbot import answer_query
from seed import seed_database

app = Flask(__name__)

_secret_key = os.environ.get('SECRET_KEY')
if not _secret_key:
    if os.environ.get('FLASK_ENV') == 'production':
        print("ERROR: SECRET_KEY environment variable is not set. Refusing to start in production.", file=sys.stderr)
        sys.exit(1)
    else:
        import secrets
        _secret_key = secrets.token_hex(32)
        print("WARNING: SECRET_KEY not set. Using a temporary random key (sessions will reset on restart). Set SECRET_KEY in your .env file.")

app.config['SECRET_KEY'] = _secret_key

# --- Database Configuration (Neon Cloud PostgreSQL / SQLite Fallback) ---
_raw_db_url = os.environ.get('DATABASE_URL', 'sqlite:///learnloop.db')

# Testing isolation: always use in-memory SQLite for test runs
if os.environ.get('TESTING') == '1':
    _db_url = 'sqlite:///:memory:'
else:
    # Normalize postgres:// to postgresql:// for SQLAlchemy 1.4+ compatibility
    if _raw_db_url.startswith('postgres://'):
        _db_url = _raw_db_url.replace('postgres://', 'postgresql://', 1)
    else:
        _db_url = _raw_db_url

app.config['SQLALCHEMY_DATABASE_URI'] = _db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Neon serverless PostgreSQL engine options:
# - pool_pre_ping: validates connections before use; cleanly handles Neon idle/wake-up
# - pool_recycle: recycles connections after 5 minutes to prevent stale dropped sockets
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

db.init_app(app)

# ---- Simple i18n implementation ----

def load_locale(lang):
    """Load translation JSON for the given language."""
    path = os.path.join(app.root_path, 'static', 'lang', f"{lang}.json")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def get_current_lang():
    # 1. Cookie priority (set directly when user clicks language toggle)
    cookie_lang = request.cookies.get('learnloop_lang')
    if cookie_lang in ['en', 'hi', 'kn']:
        return cookie_lang
    # 2. Session priority
    sess_lang = session.get('preferred_language')
    if sess_lang in ['en', 'hi', 'kn']:
        return sess_lang
    # 3. User database priority if authenticated
    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
        if user and user.preferred_language in ['en', 'hi', 'kn']:
            return user.preferred_language
    return 'en'

def _(key):
    """Translate *key* using the current language.
    Falls back to the key itself if not found.
    """
    lang = get_current_lang()
    # Cache per request
    if not hasattr(g, 'translations') or g.get('lang') != lang:
        g.lang = lang
        g.translations = load_locale(lang)
    return g.translations.get(key, key)

SUBJECT_TRANSLATIONS = {
    'kn': {
        'C Programming': 'ಸಿ ಪ್ರೋಗ್ರಾಮಿಂಗ್',
        'Digital Electronics': 'ಡಿಜಿಟಲ್ ಎಲೆಕ್ಟ್ರಾನಿಕ್ಸ್',
        'Engineering Mathematics': 'ಎಂಜಿನಿಯರಿಂಗ್ ಗಣಿತ',
        'Basic Electrical & Circuit Analysis': 'ಮೂಲ ವಿದ್ಯುತ್ ಮತ್ತು ಸರ್ಕ್ಯೂಟ್ ವಿಶ್ಲೇಷಣೆ'
    },
    'hi': {
        'C Programming': 'सी प्रोग्रामिंग',
        'Digital Electronics': 'डिजिटल इलेक्ट्रॉनिक्स',
        'Engineering Mathematics': 'इंजीनियरिंग गणित',
        'Basic Electrical & Circuit Analysis': 'बुनियादी इलेक्ट्रिकल और सर्किट विश्लेषण'
    }
}

TOPIC_TRANSLATIONS = {
    'kn': {
        'Arrays in C': 'ಸಿ ಯಲ್ಲಿ ಅರೇಗಳು (Arrays in C)',
        'Pointers and Memory': 'ಪಾಯಿಂಟರ್‌ಗಳು ಮತ್ತು ಮೆಮೊರಿ (Pointers & Memory)',
        'Functions and Recursion': 'ಫಂಕ್ಷನ್‌ಗಳು ಮತ್ತು ರಿಕರ್ಶನ್ (Functions & Recursion)',
        'Control Flow and Loops': 'ಕಂಟ್ರೋಲ್ ಫ್ಲೋ ಮತ್ತು ಲೂಪ್‌ಗಳು (Control Flow & Loops)',
        'Number Systems & Codes': 'ಸಂಖ್ಯಾ ಪದ್ಧತಿಗಳು & ಸಂಕೇತಗಳು',
        'Boolean Algebra & Logic Simplification': 'ಬೂಲಿಯನ್ ಬೀಜಗಣಿತ ಮತ್ತು ಲಾಜಿಕ್ ಸರಳೀಕರಣ',
        'Boolean Algebra & Logic': 'ಬೂಲಿಯನ್ ಬೀಜಗಣಿತ ಮತ್ತು ಲಾಜಿಕ್',
        'Logic Gates & Universal Realization': 'ಲಾಜಿಕ್ ಗೇಟ್‌ಗಳು ಮತ್ತು ಯುನಿವರ್ಸಲ್ ರಿಯಲೈಸೇಶನ್',
        'Combinational Logic Circuits': 'ಕಾಂಬಿನೇಶನಲ್ ಲಾಜಿಕ್ ಸರ್ಕ್ಯೂಟ್‌ಗಳು',
        'Matrices & Linear Systems': 'ಮ್ಯಾಟ್ರಿಕ್ಸ್‌ಗಳು & ರೇಖೀಯ ವ್ಯವಸ್ಥೆಗಳು',
        'Differential Calculus': 'ಡಿಫರೆನ್ಷಿಯಲ್ ಕಲನಶಾಸ್ತ್ರ',
        'Integral Calculus': 'ಇಂಟಿಗ್ರಲ್ ಕಲನಶಾಸ್ತ್ರ',
        'Ohm\'s & Kirchhoff\'s Laws': 'ಓಮ್ಸ್ & ಕಿರ್ಚಾಫ್ಸ್ ನಿಯಮಗಳು',
        'Series-Parallel Circuit Analysis': 'ಸರಣಿ-ಸಮಾನಾಂತರ ಸರ್ಕ್ಯೂಟ್ ವಿಶ್ಲೇಷಣೆ',
        'Mesh & Nodal Analysis': 'ಮೆಶ್ & ನೋಡಲ್ ವಿಶ್ಲೇಷಣೆ'
    },
    'hi': {
        'Arrays in C': 'C में एरे (Arrays in C)',
        'Pointers and Memory': 'पॉइंटर्स और मेमोरी (Pointers & Memory)',
        'Functions and Recursion': 'फ़ंक्शन और रिकर्शन (Functions & Recursion)',
        'Control Flow and Loops': 'कंट्रोल फ्लो और लूप्स (Control Flow & Loops)',
        'Number Systems & Codes': 'संख्या प्रणाली और कोड',
        'Boolean Algebra & Logic Simplification': 'बूलियन बीजगणित और तर्क सरलीकरण',
        'Boolean Algebra & Logic': 'बूलियन बीजगणित और तर्क',
        'Logic Gates & Universal Realization': 'लॉजिक गेट्स और सार्वभौमिक अहसास',
        'Combinational Logic Circuits': 'संयोजन तर्क सर्किट',
        'Matrices & Linear Systems': 'मैट्रिसेस और रैखिक प्रणाली',
        'Differential Calculus': 'अवकलन गणित',
        'Integral Calculus': 'समाकलन गणित',
        'Ohm\'s & Kirchhoff\'s Laws': 'ओम और किरचॉफ के नियम',
        'Series-Parallel Circuit Analysis': 'श्रृंखला-समानांतर सर्किट विश्लेषण',
        'Mesh & Nodal Analysis': 'मेश और नोडल विश्लेषण'
    }
}

PATTERN_TRANSLATIONS = {
    'kn': {
        'Core Concept Summary: ': 'ಮೂಲ ಪರಿಕಲ್ಪನೆಯ ಸಾರಾಂಶ: ',
        'Video Lecture: ': 'ವಿಡಿಯೋ ಉಪನ್ಯಾಸ: ',
        'Step-by-Step Worked Problem: ': 'ಹಂತ-ಹಂತವಾಗಿ ಪರಿಹರಿಸಿದ ಸಮಸ್ಯೆ: ',
        'Challenge Practice Problem Set: ': 'ಸವಾಲಿನ ಅಭ್ಯಾಸ ಸಮಸ್ಯೆಗಳ ಸೆಟ್: ',
        ' Explained': ' ವಿವರಣೆ',
        'Concise engineering lecture notes covering fundamental principles, key definitions, and VTU exam highlights for ': 'ಮೂಲ ತತ್ವಗಳು, ಪ್ರಮುಖ ವ್ಯಾಖ್ಯಾನಗಳು ಮತ್ತು ವಿಟಿಯು ಪರೀಕ್ಷಾ ಮುಖ್ಯಾಂಶಗಳನ್ನು ಒಳಗೊಂಡ ಸಂಕ್ಷಿಪ್ತ ಎಂಜಿನಿಯರಿಂಗ್ ಉಪನ್ಯಾಸ ಟಿಪ್ಪಣಿಗಳು: ',
        'Curated engineering video lecture and step-by-step visual demonstration for ': 'ಆಯ್ದ ಎಂಜಿನಿಯರಿಂಗ್ ವಿಡಿಯೋ ಉಪನ್ಯಾಸ ಮತ್ತು ಹಂತ-ಹಂತದ ಪ್ರಾತ್ಯಕ್ಷಿಕೆ: ',
        'Fully worked VTU-standard numerical/code example demonstrating application of ': 'ಅನ್ವಯಿಕತೆಯನ್ನು ಪ್ರದರ್ಶಿಸುವ ಸಂಪೂರ್ಣವಾಗಿ ಪರಿಹರಿಸಿದ ವಿಟಿಯು ಗುಣಮಟ್ಟದ ಸಂಖ್ಯಾತ್ಮಕ/ಕೋಡ್ ಉದಾಹರಣೆ: ',
        'Higher-order thinking questions and exam-style problem scenarios for ': 'ಉನ್ನತ ಮಟ್ಟದ ಚಿಂತನೆಯ ಪ್ರಶ್ನೆಗಳು ಮತ್ತು ಪರೀಕ್ಷಾ ಶೈಲಿಯ ಸಮಸ್ಯೆ ಸನ್ನಿವೇಶಗಳು: ',
        'notes': 'ಟಿಪ್ಪಣಿಗಳು',
        'video': 'ವಿಡಿಯೋ',
        'example': 'ಉದಾಹರಣೆ',
        'practice': 'ಅಭ್ಯಾಸ',
        'easy': 'ಸುಲಭ',
        'Easy': 'ಸುಲಭ',
        'medium': 'ಮಧ್ಯಮ',
        'Medium': 'ಮಧ್ಯಮ',
        'hard': 'ಕಠಿಣ',
        'Hard': 'ಕಠಿಣ',
        'Needs Attention': 'ಗಮನ ಹರಿಸಬೇಕಾಗಿದೆ',
        'On Track': 'ಉತ್ತಮ ಪ್ರಗತಿಯಲ್ಲಿದೆ',
        'No attempts': 'ಯಾವುದೇ ಪ್ರಯತ್ನಗಳಿಲ್ಲ',
        'Class Avg': 'ತರಗತಿ ಸರಾಸರಿ',
        'Low Mastery': 'ಕಡಿಮೆ ಪರಿಣತಿ',
        'Inspect Materials →': 'ಸಾಮಗ್ರಿಗಳನ್ನು ಪರಿಶೀಲಿಸಿ →',
        'student(s)': 'ವಿದ್ಯಾರ್ಥಿ(ಗಳು)',
        'total attempts': 'ಒಟ್ಟು ಪ್ರಯತ್ನಗಳು'
    },
    'hi': {
        'Core Concept Summary: ': 'मूल अवधारणा सारांश: ',
        'Video Lecture: ': 'वीडियो व्याख्यान: ',
        'Step-by-Step Worked Problem: ': 'चरण-दर-चरण हल की गई समस्या: ',
        'Challenge Practice Problem Set: ': 'चुनौती अभ्यास समस्या सेट: ',
        ' Explained': ' की व्याख्या',
        'Concise engineering lecture notes covering fundamental principles, key definitions, and VTU exam highlights for ': 'मूल सिद्धांतों, प्रमुख परिभाषाओं और VTU परीक्षा के मुख्य अंशों को शामिल करते संक्षिप्त इंजीनियरिंग व्याख्यान नोट्स: ',
        'Curated engineering video lecture and step-by-step visual demonstration for ': 'चयनित इंजीनियरिंग वीडियो व्याख्यान और चरण-दर-चरण दृश्य प्रदर्शन: ',
        'Fully worked VTU-standard numerical/code example demonstrating application of ': 'उपयोग प्रदर्शित करने वाला पूर्णतः हल किया गया VTU-मानक संख्यात्मक/कोड उदाहरण: ',
        'Higher-order thinking questions and exam-style problem scenarios for ': 'उच्च-स्तरीय विचारणीय प्रश्न और परीक्षा-शैली परिदृश्य: ',
        'notes': 'नोट्स',
        'video': 'वीडियो',
        'example': 'उदाहरण',
        'practice': 'अभ्यास',
        'easy': 'सरल',
        'Easy': 'सरल',
        'medium': 'मध्यम',
        'Medium': 'मध्यम',
        'hard': 'कठिन',
        'Hard': 'कठिन',
        'Needs Attention': 'ध्यान देने की आवश्यकता',
        'On Track': 'सही रास्ते पर',
        'No attempts': 'कोई प्रयास नहीं',
        'Class Avg': 'कक्षा औसत',
        'Low Mastery': 'कम दक्षता',
        'Inspect Materials →': 'अध्ययन सामग्री देखें →',
        'student(s)': 'छात्र',
        'total attempts': 'कुल प्रयास'
    }
}

def localize_text(text):
    if not text:
        return text
    lang = get_current_lang()
    if lang == 'en':
        return text
    
    # 1. Direct dictionary match
    loc = load_locale(lang)
    if text in loc:
        return loc[text]
    
    # 2. Subject match
    sub_map = SUBJECT_TRANSLATIONS.get(lang, {})
    if text in sub_map:
        return sub_map[text]
    
    # 3. Topic match
    top_map = TOPIC_TRANSLATIONS.get(lang, {})
    if text in top_map:
        return top_map[text]
    
    # 4. Pattern matches (Titles & Descriptions)
    patterns = PATTERN_TRANSLATIONS.get(lang, {})
    if text in patterns:
        return patterns[text]
    
    for prefix, trans_prefix in patterns.items():
        if text.startswith(prefix):
            remainder = text[len(prefix):]
            suffix = ' Explained'
            if remainder.endswith(suffix):
                topic_part = remainder[:-len(suffix)]
                translated_topic = top_map.get(topic_part, topic_part)
                trans_suffix = patterns.get(suffix, suffix)
                return f"{trans_prefix}{translated_topic}{trans_suffix}"
            
            dot_suffix = '.'
            has_dot = remainder.endswith(dot_suffix)
            topic_part = remainder[:-1] if has_dot else remainder
            translated_topic = top_map.get(topic_part, topic_part)
            return f"{trans_prefix}{translated_topic}{'.' if has_dot else ''}"

    return text

# expose _ and localize to Jinja templates
app.jinja_env.globals['_'] = _
app.jinja_env.filters['localize'] = localize_text
app.jinja_env.globals['localize'] = localize_text

@app.route('/set_language/<lang>')
def set_language(lang):
    if lang not in ['en', 'hi', 'kn']:
        lang = 'en'
    session['preferred_language'] = lang
    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
        if user:
            user.preferred_language = lang
            db.session.commit()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.args.get('format') == 'json':
        resp = jsonify({'status': 'ok', 'lang': lang})
    else:
        flash(f'Language switched to {lang.upper()}.', 'success')
        resp = redirect(request.referrer or url_for('index'))
    resp.set_cookie('learnloop_lang', lang, max_age=30*86400, path='/', samesite='Lax')
    return resp

@app.after_request
def set_language_cookie(response):
    lang = get_current_lang()
    if request.cookies.get('learnloop_lang') != lang:
        response.set_cookie('learnloop_lang', lang, max_age=30*86400, path='/', samesite='Lax')
    return response

@app.route('/api/translations/<lang>')
def api_translations(lang):
    if lang not in ['en', 'hi', 'kn']:
        lang = 'en'
    return jsonify(load_locale(lang))

# ---- End of i18n ----

# Ensure database tables and initial seed data exist
with app.app_context():
    db.create_all()
    if not Subject.query.first():
        seed_database(app)

# -----------------------------------------------------------------------------
# Auth Helpers & Decorators
# -----------------------------------------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please sign in to access this feature.", "warning")
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please sign in with a faculty account to access the teacher view.", "warning")
            return redirect(url_for('login', next=request.url))
        if session.get('role') != 'teacher':
            flash("Access restricted. The Teacher Oversight Portal is only accessible to verified faculty accounts.", "error")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_user_state():
    """Injects active user and preferred language into all templates."""
    active_user = None
    if 'user_id' in session:
        active_user = db.session.get(User, session['user_id'])
    lang = get_current_lang()
    session['preferred_language'] = lang
    return {
        'current_user': active_user,
        'user_lang': lang,
        '_': _
    }




# -----------------------------------------------------------------------------
# First Page / Login & Authentication Routes
# -----------------------------------------------------------------------------
def process_login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['role'] = user.role
            session['preferred_language'] = user.preferred_language
            flash(f"Welcome back, {user.name}!", "success")

            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            if user.role == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password. Please verify your credentials or choose a test demo account.", "error")

    # If already logged in and visiting via GET, redirect to their dashboard
    if 'user_id' in session and request.method == 'GET':
        if session.get('role') == 'teacher':
            return redirect(url_for('teacher_dashboard'))
        return redirect(url_for('dashboard'))

    subjects = Subject.query.all()
    total_topics = Topic.query.count()
    total_questions = Question.query.count()
    return render_template(
        'index.html',
        subjects=subjects,
        total_topics=total_topics,
        total_questions=total_questions
    )


@app.route('/', methods=['GET', 'POST'])
def index():
    return process_login()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return process_login()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        pref_lang = request.form.get('preferred_language', 'en')
        consent = request.form.get('consent')

        if not name or not email or not password:
            flash("Please fill in all required fields.", "error")
            return render_template('register.html')

        if not consent:
            flash("You must agree to the academic data consent terms to register.", "error")
            return render_template('register.html')

        existing = User.query.filter_by(email=email).first()
        if existing:
            flash("An account with that email already exists. Please sign in.", "warning")
            return redirect(url_for('login'))

        new_user = User(
            name=name,
            email=email,
            role='student',
            preferred_language=pref_lang,
            is_synthetic=False
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        session['user_name'] = new_user.name
        session['role'] = new_user.role
        session['preferred_language'] = new_user.preferred_language

        flash("Registration successful! Welcome to Learnloop.", "success")
        return redirect(url_for('topics'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been signed out successfully.", "info")
    return redirect(url_for('index'))


# -----------------------------------------------------------------------------
# Topic Browser & Course Explorer
# -----------------------------------------------------------------------------
@app.route('/topics')
def topics():
    subjects = Subject.query.all()
    user_id = session.get('user_id')

    # Build topic progress map for current user
    progress_map = {}
    last_score_map = {}
    if user_id:
        progress_records = TopicProgress.query.filter_by(user_id=user_id).all()
        for p in progress_records:
            progress_map[p.topic_id] = p

        # Retrieve last score for each topic
        for sub in subjects:
            for t in sub.topics:
                last_att = Attempt.query.filter_by(user_id=user_id, topic_id=t.id)\
                                        .order_by(Attempt.taken_at.desc()).first()
                if last_att:
                    last_score_map[t.id] = last_att.score_pct

    return render_template(
        'topics.html',
        subjects=subjects,
        progress_map=progress_map,
        last_score_map=last_score_map
    )


# -----------------------------------------------------------------------------
# Adaptive Quiz Module
# -----------------------------------------------------------------------------
@app.route('/quiz/<int:topic_id>', methods=['GET'])
@login_required
def take_quiz(topic_id):
    topic = db.session.get(Topic, topic_id)
    if not topic:
        abort(404)

    user_id = session['user_id']

    # Retrieve topic progress and last attempt to select adaptive difficulty mix
    progress = TopicProgress.query.filter_by(user_id=user_id, topic_id=topic_id).first()
    last_attempt = Attempt.query.filter_by(user_id=user_id, topic_id=topic_id)\
                                .order_by(Attempt.taken_at.desc()).first()

    current_mastery = progress.mastery_level if progress else 'Low'
    last_score = last_attempt.score_pct if last_attempt else None

    # Compute next difficulty mix using rule-based engine
    diff_mix = next_difficulty(current_mastery, last_score)

    # Fetch pool of questions matching difficulty requirements
    easy_pool = Question.query.filter_by(topic_id=topic_id, difficulty='easy').all()
    med_pool = Question.query.filter_by(topic_id=topic_id, difficulty='medium').all()
    hard_pool = Question.query.filter_by(topic_id=topic_id, difficulty='hard').all()

    selected_questions = []
    # Pick questions according to mix
    selected_questions.extend(random.sample(easy_pool, min(diff_mix['easy'], len(easy_pool))))
    selected_questions.extend(random.sample(med_pool, min(diff_mix['medium'], len(med_pool))))
    selected_questions.extend(random.sample(hard_pool, min(diff_mix['hard'], len(hard_pool))))

    # If count is less than 5, backfill from remaining pool
    if len(selected_questions) < 5:
        all_pool = Question.query.filter_by(topic_id=topic_id).all()
        remaining = [q for q in all_pool if q not in selected_questions]
        needed = 5 - len(selected_questions)
        selected_questions.extend(random.sample(remaining, min(needed, len(remaining))))

    random.shuffle(selected_questions)

    # Prepare question payloads (without answers, to ensure secure client delivery)
    quiz_questions = [q.to_dict(include_answer=False) for q in selected_questions]

    diff_mix_label = f"{diff_mix['easy']} easy, {diff_mix['medium']} medium, {diff_mix['hard']} hard"

    return render_template(
        'quiz.html',
        topic=topic,
        questions=quiz_questions,
        difficulty_mix=diff_mix_label,
        current_mastery=current_mastery
    )


@app.route('/quiz/<int:topic_id>/submit', methods=['POST'])
@login_required
def submit_quiz(topic_id):
    topic = db.session.get(Topic, topic_id)
    if not topic:
        abort(404)

    user_id = session['user_id']
    difficulty_mix = request.form.get('difficulty_mix', 'adaptive')

    # Server-side verification of answers
    results = []
    missed_subtopics = set()
    detailed_answers = []

    # Iterate through submitted question answers
    for key, chosen_opt in request.form.items():
        if key.startswith('q_'):
            q_id = int(key.replace('q_', ''))
            question = db.session.get(Question, q_id)
            if question and question.topic_id == topic_id:
                is_correct = (chosen_opt.strip().upper() == question.correct_option.strip().upper())
                results.append({'is_correct': is_correct})

                if not is_correct and question.subtopic:
                    missed_subtopics.add(question.subtopic)

                detailed_answers.append({
                    'question_id': question.id,
                    'text': question.text,
                    'chosen_option': chosen_opt.upper(),
                    'correct_option': question.correct_option,
                    'is_correct': is_correct,
                    'explanation': question.explanation,
                    'options': {
                        'A': question.option_a,
                        'B': question.option_b,
                        'C': question.option_c,
                        'D': question.option_d
                    }
                })

    score_pct = compute_attempt_score(results)

    # 1. Record Attempt in DB
    attempt = Attempt(
        user_id=user_id,
        topic_id=topic_id,
        score_pct=score_pct,
        difficulty_mix=difficulty_mix,
        taken_at=utc_now()
    )
    db.session.add(attempt)
    db.session.flush()

    # 2. Record Attempt Answers
    for ans in detailed_answers:
        att_ans = AttemptAnswer(
            attempt_id=attempt.id,
            question_id=ans['question_id'],
            chosen_option=ans['chosen_option'],
            is_correct=ans['is_correct']
        )
        db.session.add(att_ans)

    # 3. Calculate Weighted Topic Mastery using engine
    past_attempts = Attempt.query.filter_by(user_id=user_id, topic_id=topic_id)\
                                 .order_by(Attempt.taken_at.asc()).all()
    mastery_calc = topic_mastery(past_attempts)

    # 4. Update or Create TopicProgress
    progress = TopicProgress.query.filter_by(user_id=user_id, topic_id=topic_id).first()
    if not progress:
        progress = TopicProgress(
            user_id=user_id,
            topic_id=topic_id,
            mastery_level=mastery_calc['mastery_level'],
            mastery_pct=mastery_calc['mastery_pct'],
            completed=(score_pct >= 40.0),
            last_updated=utc_now()
        )
        db.session.add(progress)
    else:
        progress.mastery_level = mastery_calc['mastery_level']
        progress.mastery_pct = mastery_calc['mastery_pct']
        if score_pct >= 40.0:
            progress.completed = True
        progress.last_updated = utc_now()

    db.session.commit()

    # 5. Generate Adaptive Recommendations
    rec = recommend(
        topic_name=topic.name,
        mastery_level=mastery_calc['mastery_level'],
        score_pct=score_pct,
        missed_subtopics=list(missed_subtopics)
    )

    # 6. Retrieve relevant resources for this topic
    recommended_resources = []
    for res_type in rec['recommended_sequence']:
        r = Resource.query.filter_by(topic_id=topic_id, type=res_type).first()
        if r and r not in recommended_resources:
            recommended_resources.append(r)

    # Render result view inside quiz.html
    return render_template(
        'quiz.html',
        topic=topic,
        is_result=True,
        score_pct=score_pct,
        mastery_calc=mastery_calc,
        recommendation=rec,
        recommended_resources=recommended_resources,
        detailed_answers=detailed_answers
    )


# -----------------------------------------------------------------------------
# Resource Repository
# -----------------------------------------------------------------------------
@app.route('/resources')
def resources():
    subjects = Subject.query.all()
    sub_id = request.args.get('subject_id', type=int)
    top_id = request.args.get('topic_id', type=int)
    res_type = request.args.get('type')
    search_q = request.args.get('q', '').strip()

    query = Resource.query.join(Topic)

    if sub_id:
        query = query.filter(Topic.subject_id == sub_id)
    if top_id:
        query = query.filter(Resource.topic_id == top_id)
    if res_type:
        query = query.filter(Resource.type == res_type)
    if search_q:
        search_filter = f"%{search_q}%"
        query = query.filter((Resource.title.ilike(search_filter)) | (Resource.description.ilike(search_filter)))

    all_resources = query.all()

    return render_template(
        'resources.html',
        resources=all_resources,
        subjects=subjects,
        selected_sub=sub_id,
        selected_topic=top_id,
        selected_type=res_type,
        search_q=search_q
    )


@app.route('/resource/<int:resource_id>')
def view_resource(resource_id):
    resource = db.session.get(Resource, resource_id)
    if not resource:
        abort(404)

    # Record resource view if student is logged in
    if 'user_id' in session:
        user_id = session['user_id']
        rv = ResourceView(user_id=user_id, resource_id=resource.id, viewed_at=utc_now())
        db.session.add(rv)

        # Mark topic completion if student reads resources
        prog = TopicProgress.query.filter_by(user_id=user_id, topic_id=resource.topic_id).first()
        if prog:
            prog.completed = True
            prog.last_updated = utc_now()
        db.session.commit()

    return render_template('resource_detail.html', resource=resource)


# -----------------------------------------------------------------------------
# Student Analytics Dashboard
# -----------------------------------------------------------------------------
@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    user = db.session.get(User, user_id)

    # Topics completed count
    completed_topics_count = TopicProgress.query.filter_by(user_id=user_id, completed=True).count()
    total_topics_count = Topic.query.count()

    # User's attempts
    attempts = Attempt.query.filter_by(user_id=user_id).order_by(Attempt.taken_at.desc()).all()
    total_attempts = len(attempts)

    # Average score
    avg_score = round(sum(a.score_pct for a in attempts) / total_attempts, 1) if total_attempts > 0 else 0.0

    # Topic Progress list
    progress_records = TopicProgress.query.filter_by(user_id=user_id).all()
    progress_dict = {p.topic_id: p for p in progress_records}

    # Strengths (High) and Gaps (Low/Medium)
    strengths = []
    gaps = []
    for p in progress_records:
        if p.mastery_level == 'High':
            strengths.append(p)
        else:
            gaps.append(p)

    # Overall mastery band
    if not progress_records:
        overall_mastery = "Not Started"
    else:
        avg_mastery_pct = sum(p.mastery_pct for p in progress_records) / len(progress_records)
        overall_mastery = get_mastery_band(avg_mastery_pct)

    # Prepare Chart Data:
    # 1. Bar Chart: Topics & Mastery %
    topics_all = Topic.query.all()
    chart_topic_labels = [t.name for t in topics_all]
    chart_topic_scores = [progress_dict[t.id].mastery_pct if t.id in progress_dict else 0 for t in topics_all]

    # 2. Line Chart: Chronological score trend (last 10 attempts)
    recent_chronological = Attempt.query.filter_by(user_id=user_id).order_by(Attempt.taken_at.asc()).limit(15).all()
    chart_trend_labels = [f"Attempt {i+1} ({a.topic.name[:12]}..)" for i, a in enumerate(recent_chronological)]
    chart_trend_scores = [a.score_pct for a in recent_chronological]

    return render_template(
        'dashboard.html',
        user=user,
        completed_count=completed_topics_count,
        total_topics=total_topics_count,
        total_attempts=total_attempts,
        avg_score=avg_score,
        overall_mastery=overall_mastery,
        strengths=strengths,
        gaps=gaps,
        attempts=attempts[:10],
        chart_topic_labels=chart_topic_labels,
        chart_topic_scores=chart_topic_scores,
        chart_trend_labels=chart_trend_labels,
        chart_trend_scores=chart_trend_scores
    )


# -----------------------------------------------------------------------------
# Teacher Oversight Portal (Read-Only)
# -----------------------------------------------------------------------------
@app.route('/teacher')
@teacher_required
def teacher_dashboard():
    # 1. Topic class averages and low-mastery counts
    topics = Topic.query.all()
    topic_stats = []

    for t in topics:
        topic_attempts = Attempt.query.filter_by(topic_id=t.id).all()
        avg_pct = round(sum(a.score_pct for a in topic_attempts) / len(topic_attempts), 1) if topic_attempts else None
        
        # Count students with Low mastery
        low_count = TopicProgress.query.filter_by(topic_id=t.id, mastery_level='Low').count()
        total_tested = TopicProgress.query.filter_by(topic_id=t.id).count()

        topic_stats.append({
            'topic': t,
            'attempts_count': len(topic_attempts),
            'avg_score': avg_pct,
            'low_count': low_count,
            'total_tested': total_tested,
            'needs_attention': (low_count >= 1) or (avg_pct is not None and avg_pct < 50.0)
        })

    # 2. Latest scores per student
    students = User.query.filter_by(role='student').all()
    student_summaries = []
    for s in students:
        s_attempts = Attempt.query.filter_by(user_id=s.id).order_by(Attempt.taken_at.desc()).all()
        s_avg = round(sum(a.score_pct for a in s_attempts) / len(s_attempts), 1) if s_attempts else 0.0
        s_last = s_attempts[0] if s_attempts else None
        student_summaries.append({
            'student': s,
            'attempts_count': len(s_attempts),
            'avg_score': s_avg,
            'last_attempt': s_last
        })

    return render_template(
        'teacher.html',
        topic_stats=topic_stats,
        student_summaries=student_summaries
    )


@app.route('/teacher/clear-student-data', methods=['POST'])
@teacher_required
def clear_student_data():
    action = request.form.get('action', 'clear_all')
    student_id = request.form.get('student_id', type=int)

    if action == 'clear_all':
        # Clear all attempts, attempt answers, topic progress, and resource views
        AttemptAnswer.query.delete()
        Attempt.query.delete()
        TopicProgress.query.delete()
        ResourceView.query.delete()
        db.session.commit()
        flash("All student diagnostic quiz records, attempt histories, and progress data have been cleared successfully.", "success")
        return redirect(url_for('teacher_dashboard'))

    elif action == 'reset_student' and student_id:
        student = db.session.get(User, student_id)
        if student and student.role == 'student':
            student_attempts = Attempt.query.filter_by(user_id=student.id).all()
            for att in student_attempts:
                db.session.delete(att)
            TopicProgress.query.filter_by(user_id=student.id).delete()
            ResourceView.query.filter_by(user_id=student.id).delete()
            db.session.commit()
            flash(f"Progress and attempt records for student '{student.name}' have been cleared.", "success")
        else:
            flash("Student record not found or cannot be modified.", "error")
        return redirect(url_for('teacher_dashboard'))

    elif action == 'delete_student' and student_id:
        student = db.session.get(User, student_id)
        if student and student.role == 'student':
            name = student.name
            db.session.delete(student)
            db.session.commit()
            flash(f"Student account '{name}' and all associated records have been removed successfully.", "success")
        else:
            flash("Cannot delete this user account.", "error")
        return redirect(url_for('teacher_dashboard'))

    flash("Invalid action specified.", "error")
    return redirect(url_for('teacher_dashboard'))


# -----------------------------------------------------------------------------
# Multilingual AI-Integrated Chatbot JSON API
# -----------------------------------------------------------------------------
@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json() or {}
    query_text = data.get('message', '').strip()
    requested_lang = data.get('lang', session.get('preferred_language', 'en'))
    api_key = data.get('api_key') or request.headers.get('X-AI-API-Key') or session.get('ai_api_key') or os.environ.get('GEMINI_API_KEY') or os.environ.get('AI_API_KEY') or os.environ.get('OPENAI_API_KEY')

    result = answer_query(query_text, requested_lang=requested_lang, api_key=api_key)

    # Anonymized logging (no student identifiers)
    log_entry = ChatLog(
        language=result['lang'],
        query_text=query_text[:500],
        matched=result['matched'],
        created_at=utc_now()
    )
    db.session.add(log_entry)
    db.session.commit()

    return jsonify({
        'answer': result['answer'],
        'matched': result['matched'],
        'lang': result['lang'],
        'confidence': result.get('confidence', 0.0),
        'source': result.get('source', 'knowledge_base')
    })


@app.route('/api/set-api-key', methods=['POST'])
def api_set_key():
    data = request.get_json() or {}
    key = data.get('api_key', '').strip()
    if key:
        session['ai_api_key'] = key
        return jsonify({'success': True, 'message': 'AI API key saved for this session.'})
    else:
        session.pop('ai_api_key', None)
        return jsonify({'success': True, 'message': 'AI API key removed from session.'})



# -----------------------------------------------------------------------------
# Error Handlers
# -----------------------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('404.html'), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', '0').lower() in ('1', 'true', 't')
    host = '0.0.0.0' if os.environ.get('PORT') else '127.0.0.1'

    if debug_mode:
        app.run(host=host, port=port, debug=True)
    else:
        try:
            from waitress import serve
            print(f" * Serving production WSGI with Waitress on http://{host}:{port}", flush=True)
            serve(app, host=host, port=port)
        except ImportError:
            app.run(host=host, port=port, debug=False)

