import pytest
import sqlite3
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services import add_student, get_all_students, get_student_by_id, delete_student, get_student_by_roll


@pytest.fixture
def db():
    """Create a fresh in-memory SQLite database for each test."""
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


def test_add_student_saves_to_db(db):
    """Adding a student should store them in the database."""
    add_student(db, "Rahul Sharma", "CS001", 85, 90, 78)
    students = get_all_students(db)
    assert len(students) == 1
    assert students[0]["name"] == "Rahul Sharma"


def test_add_student_calculates_grade(db):
    """Adding a student should auto-calculate percentage and grade."""
    result = add_student(db, "Priya Patel", "CS002", 95, 92, 98)
    assert result["grade"] == "A+"
    assert result["percentage"] == 95.0


def test_add_student_duplicate_roll_raises_error(db):
    """Adding two students with same roll number should raise ValueError."""
    add_student(db, "Student One", "CS001", 80, 80, 80)
    with pytest.raises(ValueError):
        add_student(db, "Student Two", "CS001", 70, 70, 70)


def test_add_student_empty_name_raises_error(db):
    """Adding a student with empty name should raise ValueError."""
    with pytest.raises(ValueError):
        add_student(db, "", "CS005", 80, 80, 80)


def test_get_all_students_returns_sorted_by_percentage(db):
    """Students should be returned sorted by percentage descending."""
    add_student(db, "Low Scorer", "CS010", 40, 45, 50)
    add_student(db, "High Scorer", "CS011", 95, 90, 92)
    students = get_all_students(db)
    assert students[0]["name"] == "High Scorer"
    assert students[1]["name"] == "Low Scorer"


def test_get_student_by_id_returns_correct(db):
    """Should return the correct student for a given ID."""
    add_student(db, "Anjali Singh", "CS020", 75, 80, 70)
    all_s = get_all_students(db)
    sid = all_s[0]["id"]
    student = get_student_by_id(db, sid)
    assert student["name"] == "Anjali Singh"


def test_get_student_by_id_returns_none_for_missing(db):
    """Should return None for a non-existent ID."""
    result = get_student_by_id(db, 9999)
    assert result is None


def test_delete_student_removes_record(db):
    """Deleting a student should remove them from the database."""
    add_student(db, "Delete Me", "CS099", 60, 60, 60)
    sid = get_all_students(db)[0]["id"]
    result = delete_student(db, sid)
    assert result is True
    assert len(get_all_students(db)) == 0


def test_delete_student_returns_false_for_missing(db):
    """Deleting a non-existent ID should return False."""
    result = delete_student(db, 9999)
    assert result is False


def test_get_student_by_roll_number(db):
    """Should find a student using their roll number."""
    add_student(db, "Vikram Rao", "CS030", 88, 92, 85)
    student = get_student_by_roll(db, "CS030")
    assert student is not None
    assert student["name"] == "Vikram Rao"
