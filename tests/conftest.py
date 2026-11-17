import os

# Ensure all pytest executions strictly use an isolated, ephemeral in-memory SQLite database.
# This guarantees tests never connect to or modify the live Neon cloud PostgreSQL database.
os.environ['TESTING'] = '1'
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
