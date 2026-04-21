import pytest
import sqlite3
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services import add_student, get_class_statistics


@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE students (
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
    conn.commit()
    yield conn
    conn.close()


def test_stats_empty_database(db):
    """Stats should return zeros when no students exist."""
    stats = get_class_statistics(db)
    assert stats["total"] == 0
    assert stats["average"] == 0


def test_stats_total_count(db):
    """Total should reflect number of students added."""
    add_student(db, "Student A", "S001", 80, 80, 80)
    add_student(db, "Student B", "S002", 70, 70, 70)
    stats = get_class_statistics(db)
    assert stats["total"] == 2


def test_stats_pass_fail_count(db):
    """Pass/fail count should be correctly calculated."""
    add_student(db, "Passing Student", "S001", 60, 60, 60)   # 60% → C (pass)
    add_student(db, "Failing Student", "S002", 30, 40, 35)   # ~35% → F (fail)
    stats = get_class_statistics(db)
    assert stats["pass_count"] == 1
    assert stats["fail_count"] == 1


def test_stats_highest_and_lowest(db):
    """Highest and lowest percentages should be correct."""
    add_student(db, "Top Student", "S001", 100, 100, 100)   # 100%
    add_student(db, "Low Student", "S002", 10, 10, 10)       # 10%
    stats = get_class_statistics(db)
    assert stats["highest"] == 100.0
    assert stats["lowest"] == 10.0
