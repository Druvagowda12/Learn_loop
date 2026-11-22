#!/usr/bin/env python3
"""
Populate Complete Trilingual Study Notes into Database
======================================================
Synchronizes complete 4-section VTU study notes across all 14 topics:
- English (content)
- Kannada (content_kn)
- Hindi (content_hi)
Updates both Resource (type='notes') and Lesson records.
"""

import os
import sys

# Ensure root directory is on Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Topic, Resource, Lesson, Module
from data.complete_study_notes import COMPLETE_STUDY_NOTES


def populate_study_notes():
    with app.app_context():
        print("Starting synchronization of Complete Trilingual Study Notes...")
        topics = Topic.query.all()
        topic_map = {t.name: t for t in topics}

        updated_resources = 0
        created_resources = 0
        updated_lessons = 0

        for topic_name, notes_data in COMPLETE_STUDY_NOTES.items():
            topic = topic_map.get(topic_name)
            if not topic:
                print(f"[WARN] Topic '{topic_name}' not found in database! Skipping.")
                continue

            # 1. Update or create Resource of type 'notes'
            res = Resource.query.filter_by(topic_id=topic.id, type='notes').first()
            if not res:
                res = Resource(
                    topic_id=topic.id,
                    type='notes',
                    target_level='low',
                    difficulty='easy',
                    needs_review=False
                )
                db.session.add(res)
                created_resources += 1
            else:
                updated_resources += 1

            res.title = notes_data['title']
            res.title_kn = notes_data['title_kn']
            res.title_hi = notes_data['title_hi']
            res.description = notes_data['desc']
            res.description_kn = notes_data['desc_kn']
            res.description_hi = notes_data['desc_hi']
            res.content = notes_data['content_en']
            res.content_kn = notes_data['content_kn']
            res.content_hi = notes_data['content_hi']

            # 2. Also synchronize corresponding Lesson records if modules exist
            lessons = Lesson.query.filter(Lesson.title.ilike(f"%{topic_name}%")).all()
            for lesson in lessons:
                lesson.notes_en = notes_data['content_en']
                lesson.notes_kn = notes_data['content_kn']
                lesson.notes_hi = notes_data['content_hi']
                updated_lessons += 1

        db.session.commit()
        print(f"\n[SUCCESS] Resources synchronized: {updated_resources} updated, {created_resources} created.")
        print(f"[SUCCESS] Lessons synchronized: {updated_lessons} updated.")

        # Verification check
        print("\nVerifying database notes lengths across all 14 topics:")
        print(f"{'ID':<4} | {'Topic Name':<35} | {'EN Chars':<10} | {'KN Chars':<10} | {'HI Chars':<10}")
        print("-" * 75)
        for t in topics:
            r = Resource.query.filter_by(topic_id=t.id, type='notes').first()
            if r:
                en_len = len(r.content or '')
                kn_len = len(r.content_kn or '')
                hi_len = len(r.content_hi or '')
                print(f"{r.id:<4} | {t.name:<35} | {en_len:<10} | {kn_len:<10} | {hi_len:<10}")


if __name__ == '__main__':
    populate_study_notes()
