import sqlite3
import click
from flask import g


def get_db(app=None):
    """Get database connection. Uses app context if available."""
    if g:
        try:
            from flask import current_app
            if "db" not in g:
                g.db = sqlite3.connect(
                    current_app.config["DATABASE"],
                    detect_types=sqlite3.PARSE_DECLTYPES
                )
                g.db.row_factory = sqlite3.Row
            return g.db
        except RuntimeError:
            pass

    # Fallback for testing outside app context
    if app:
        conn = sqlite3.connect(app.config["DATABASE"])
        conn.row_factory = sqlite3.Row
        return conn

    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn


def close_db(e=None):
    """Close database connection."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    """Initialize the database schema."""
    with app.app_context():
        db = sqlite3.connect(app.config["DATABASE"])
        db.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roll_number TEXT NOT NULL UNIQUE,
                maths INTEGER NOT NULL,
                science INTEGER NOT NULL,
                english INTEGER NOT NULL,
                percentage REAL NOT NULL,
                grade TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.commit()
        db.close()

    app.teardown_appcontext(close_db)
