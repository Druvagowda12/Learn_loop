#!/usr/bin/env python3
"""
LearnLoop Database Inspection Tool (scripts/view_db.py)
======================================================
CLI helper to inspect Neon PostgreSQL (or SQLite) tables without needing the web console:
- Users (Students & Faculty)
- Quiz Attempts & Diagnostics
- Lesson Progress
- Curriculum & Quiz Question counts per subject
"""

import os
import sys

# Ensure root directory is on Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import User, Subject, Topic, Question, Attempt, QuizAttempt, LessonProgress, Lesson


def print_banner(title: str):
    width = 75
    print("\n" + "=" * width)
    print(f" {title.upper()} ".center(width, " "))
    print("=" * width)


def print_section(title: str):
    print(f"\n--- {title} " + "-" * (70 - len(title)))


def view_database():
    with app.app_context():
        # Mask connection URL for security
        raw_url = str(db.engine.url)
        masked_url = raw_url
        if "@" in raw_url:
            creds, host_part = raw_url.split("@", 1)
            driver = creds.split("://", 1)[0]
            masked_url = f"{driver}://*****:*****@{host_part}"

        print_banner("LearnLoop Database Inspector")
        print(f" Connected Engine: {masked_url}")

        # -------------------------------------------------------------
        # 1. High-Level Metrics Summary
        # -------------------------------------------------------------
        total_users = User.query.count()
        student_count = User.query.filter_by(role='student').count()
        faculty_count = User.query.filter(User.role.in_(['faculty', 'teacher'])).count()
        total_subjects = Subject.query.count()
        total_topics = Topic.query.count()
        total_questions = Question.query.count()
        total_attempts = Attempt.query.count()
        total_quiz_attempts = QuizAttempt.query.count()
        total_lesson_progress = LessonProgress.query.count()

        print_section("Summary Overview")
        print(f" • Total Registered Users   : {total_users} (Students: {student_count}, Faculty: {faculty_count})")
        print(f" • Total Engineering Topics : {total_topics} across {total_subjects} subjects")
        print(f" • Total 4-Option Questions : {total_questions} (Trilingual: EN / KN / HI)")
        print(f" • Total Diagnostic Attempts: {total_attempts} (LMS Quiz Attempts: {total_quiz_attempts})")
        print(f" • Total Lesson Completions : {total_lesson_progress}")

        # -------------------------------------------------------------
        # 2. Subjects & Question Counts Breakdown
        # -------------------------------------------------------------
        print_section("Subjects & Question Bank Breakdown")
        subjects = Subject.query.order_by(Subject.id).all()
        header = f" {'ID':<4} | {'Subject Name':<32} | {'Topics':<8} | {'Questions':<10}"
        print(header)
        print(" " + "-" * (len(header) - 1))

        for sub in subjects:
            topics = Topic.query.filter_by(subject_id=sub.id).all()
            t_ids = [t.id for t in topics]
            q_count = Question.query.filter(Question.topic_id.in_(t_ids)).count() if t_ids else 0
            print(f" {sub.id:<4} | {sub.name:<32} | {len(topics):<8} | {q_count:<10}")

        # -------------------------------------------------------------
        # 3. Users Table
        # -------------------------------------------------------------
        print_section("Registered Users ('users')")
        users = User.query.order_by(User.id).all()
        u_header = f" {'ID':<4} | {'Name':<24} | {'Role':<9} | {'Lang':<5} | {'Attempts':<9} | {'Email':<25}"
        print(u_header)
        print(" " + "-" * (len(u_header) - 1))

        for u in users:
            u_attempts = Attempt.query.filter_by(user_id=u.id).count() + QuizAttempt.query.filter_by(user_id=u.id).count()
            print(f" {u.id:<4} | {u.name[:23]:<24} | {u.role:<9} | {u.preferred_language:<5} | {u_attempts:<9} | {u.email:<25}")

        # -------------------------------------------------------------
        # 4. Recent Quiz Attempts ('quiz_attempts')
        # -------------------------------------------------------------
        print_section("Recent Quiz Attempts ('quiz_attempts')")
        recent_qas = QuizAttempt.query.order_by(QuizAttempt.id.desc()).limit(15).all()
        if not recent_qas:
            print("  (No quiz attempt records logged yet)")
        else:
            qa_header = f" {'ID':<4} | {'User ID':<8} | {'Subject':<22} | {'Topic':<22} | {'Score %':<8} | {'Difficulty':<15}"
            print(qa_header)
            print(" " + "-" * (len(qa_header) - 1))
            for qa in recent_qas:
                diff = qa.difficulty[:14] if qa.difficulty else "adaptive"
                print(f" {qa.id:<4} | {qa.user_id:<8} | {qa.subject[:21]:<22} | {qa.topic[:21]:<22} | {qa.score_percent:<8.1f} | {diff:<15}")

        # -------------------------------------------------------------
        # 5. Lesson Progress Records ('lesson_progress')
        # -------------------------------------------------------------
        print_section("Lesson Progress Records ('lesson_progress')")
        recent_lp = LessonProgress.query.order_by(LessonProgress.id.desc()).limit(15).all()
        if not recent_lp:
            print("  (No lesson progress records logged yet)")
        else:
            lp_header = f" {'ID':<4} | {'User ID':<8} | {'Lesson Title':<35} | {'Completed':<10} | {'Completed At'}"
            print(lp_header)
            print(" " + "-" * (len(lp_header) - 1))
            for lp in recent_lp:
                lesson_title = lp.lesson.title[:34] if lp.lesson else f"Lesson #{lp.lesson_id}"
                comp_str = "Yes" if lp.completed else "In Progress"
                time_str = lp.completed_at.strftime("%Y-%m-%d %H:%M") if lp.completed_at else "-"
                print(f" {lp.id:<4} | {lp.user_id:<8} | {lesson_title:<35} | {comp_str:<10} | {time_str}")

        print("\n" + "=" * 75)
        print(" Database inspection completed successfully.\n")


if __name__ == '__main__':
    try:
        view_database()
    except Exception as e:
        print(f"\n[ERROR] Failed to query database: {e}", file=sys.stderr)
        sys.exit(1)
