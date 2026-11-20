from datetime import datetime, timezone
from typing import Any
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

def utc_now():
    return datetime.now(timezone.utc)

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

class User(BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='student', nullable=False)  # 'student' | 'teacher'
    preferred_language = db.Column(db.String(10), default='en', nullable=False)  # 'en' | 'hi' | 'kn'
    created_at = db.Column(db.DateTime, default=utc_now, nullable=False)
    is_synthetic = db.Column(db.Boolean, default=False, nullable=False)

    attempts = db.relationship('Attempt', backref='user', lazy=True, cascade='all, delete-orphan')
    progress = db.relationship('TopicProgress', backref='user', lazy=True, cascade='all, delete-orphan')
    resource_views = db.relationship('ResourceView', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'preferred_language': self.preferred_language
        }


class Subject(BaseModel):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    topics = db.relationship('Topic', backref='subject', lazy=True, cascade='all, delete-orphan')


class Topic(BaseModel):
    __tablename__ = 'topics'

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)

    questions = db.relationship('Question', backref='topic', lazy=True, cascade='all, delete-orphan')
    resources = db.relationship('Resource', backref='topic', lazy=True, cascade='all, delete-orphan')
    attempts = db.relationship('Attempt', backref='topic', lazy=True)
    progress_records = db.relationship('TopicProgress', backref='topic', lazy=True)


class Question(BaseModel):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.Text, nullable=False)
    option_b = db.Column(db.Text, nullable=False)
    option_c = db.Column(db.Text, nullable=False)
    option_d = db.Column(db.Text, nullable=False)
    option_e = db.Column(db.Text, nullable=True)  # 5th choice option E
    correct_option = db.Column(db.String(1), nullable=False)  # 'A', 'B', 'C', 'D', 'E'
    difficulty = db.Column(db.String(10), nullable=False)    # 'easy', 'medium', 'hard'
    subtopic = db.Column(db.String(100), nullable=False)
    explanation = db.Column(db.Text, nullable=False)

    # Kannada parallel content fields
    text_kn = db.Column(db.Text, nullable=True)
    option_a_kn = db.Column(db.Text, nullable=True)
    option_b_kn = db.Column(db.Text, nullable=True)
    option_c_kn = db.Column(db.Text, nullable=True)
    option_d_kn = db.Column(db.Text, nullable=True)
    option_e_kn = db.Column(db.Text, nullable=True)
    explanation_kn = db.Column(db.Text, nullable=True)
    subtopic_kn = db.Column(db.String(100), nullable=True)

    @property
    def correct_index(self) -> int:
        mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
        return mapping.get((self.correct_option or 'A').strip().upper(), 0)

    def to_dict(self, lang='en', include_answer=False):
        is_kn = (lang == 'kn')
        opt_e_val = self.option_e_kn if is_kn and self.option_e_kn else self.option_e
        if not opt_e_val:
            opt_e_val = "ಮೇಲಿನ ಯಾವುದೂ ಅಲ್ಲ" if is_kn else "None of the above"

        options_dict = {
            'A': (self.option_a_kn if is_kn and self.option_a_kn else self.option_a),
            'B': (self.option_b_kn if is_kn and self.option_b_kn else self.option_b),
            'C': (self.option_c_kn if is_kn and self.option_c_kn else self.option_c),
            'D': (self.option_d_kn if is_kn and self.option_d_kn else self.option_d),
            'E': opt_e_val
        }

        options_list = [
            options_dict['A'],
            options_dict['B'],
            options_dict['C'],
            options_dict['D'],
            options_dict['E']
        ]

        data = {
            'id': self.id,
            'topic_id': self.topic_id,
            'text': (self.text_kn if is_kn and self.text_kn else self.text),
            'options': options_dict,
            'options_list': options_list,
            'difficulty': self.difficulty,
            'subtopic': (self.subtopic_kn if is_kn and self.subtopic_kn else self.subtopic),
            'correct_index': self.correct_index,
        }
        if include_answer:
            data['correct_option'] = self.correct_option
            data['explanation'] = (self.explanation_kn if is_kn and self.explanation_kn else self.explanation)
        return data


class Attempt(BaseModel):
    __tablename__ = 'attempts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    score_pct = db.Column(db.Float, nullable=False)
    difficulty_mix = db.Column(db.String(100), nullable=True)  # e.g., '3 easy, 2 medium'
    taken_at = db.Column(db.DateTime, default=utc_now, nullable=False)

    answers = db.relationship('AttemptAnswer', backref='attempt', lazy=True, cascade='all, delete-orphan')


class AttemptAnswer(BaseModel):
    __tablename__ = 'attempt_answers'

    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('attempts.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    chosen_option = db.Column(db.String(1), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)

    question = db.relationship('Question')


class TopicProgress(BaseModel):
    __tablename__ = 'topic_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    mastery_level = db.Column(db.String(20), default='Low', nullable=False)  # 'Low', 'Medium', 'High'
    mastery_pct = db.Column(db.Float, default=0.0, nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    last_updated = db.Column(db.DateTime, default=utc_now, nullable=False)


class Resource(BaseModel):
    __tablename__ = 'resources'

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'notes', 'video', 'example', 'practice'
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(500), nullable=True)
    content = db.Column(db.Text, nullable=True)
    target_level = db.Column(db.String(20), default='low', nullable=False)  # 'low', 'medium', 'high'
    difficulty = db.Column(db.String(20), default='easy', nullable=False)   # 'easy', 'medium', 'hard'
    needs_review = db.Column(db.Boolean, default=False, nullable=False)

    # Kannada parallel content and localized video streaming
    title_kn = db.Column(db.String(250), nullable=True)
    description_kn = db.Column(db.Text, nullable=True)
    content_kn = db.Column(db.Text, nullable=True)
    url_kn = db.Column(db.String(500), nullable=True)

    views = db.relationship('ResourceView', backref='resource', lazy=True, cascade='all, delete-orphan')

    def get_title(self, lang='en') -> str:
        if lang == 'kn' and self.title_kn:
            return self.title_kn
        return self.title

    def get_description(self, lang='en') -> str:
        if lang == 'kn' and self.description_kn:
            return self.description_kn
        return self.description

    def get_content(self, lang='en') -> str:
        if lang == 'kn' and self.content_kn:
            return self.content_kn
        return self.content or ''

    def get_url(self, lang='en') -> str:
        if lang == 'kn' and self.url_kn:
            return self.url_kn
        return self.url or ''


class ResourceView(BaseModel):
    __tablename__ = 'resource_views'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'), nullable=False)
    viewed_at = db.Column(db.DateTime, default=utc_now, nullable=False)


class ChatLog(BaseModel):
    __tablename__ = 'chat_logs'

    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(10), nullable=False)
    query_text = db.Column(db.Text, nullable=False)
    matched = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now, nullable=False)
