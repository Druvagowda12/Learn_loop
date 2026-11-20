import os
import pytest

# Ensure all pytest executions strictly use an isolated, ephemeral in-memory SQLite database.
# This guarantees tests never connect to or modify the live Neon cloud PostgreSQL database.
os.environ['TESTING'] = '1'
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

from app import app, db
from seed import seed_database

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        db.create_all()
        seed_database(app)
    with app.test_client() as client:
        yield client
