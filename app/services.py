import sqlite3


def calculate_percentage(maths, science, english):
    """Calculate percentage from three subject marks."""
    total = maths + science + english
    return round(total / 3, 2)


def calculate_grade(percentage):
    """
    Assign grade based on percentage.
    A+ >= 90, A >= 80, B >= 70, C >= 60, D >= 50, F < 50
    """
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"


def validate_marks(maths, science, english):
    """Validate that all marks are between 0 and 100."""
    for subject, mark in [("Maths", maths), ("Science", science), ("English", english)]:
        if not isinstance(mark, (int, float)):
            raise ValueError(f"{subject} marks must be a number")
        if mark < 0 or mark > 100:
            raise ValueError(f"{subject} marks must be between 0 and 100")


def validate_student_data(name, roll_number, maths, science, english):
    """Validate all student input fields."""
    if not name or str(name).strip() == "":
        raise ValueError("Student name cannot be empty")
    if not roll_number or str(roll_number).strip() == "":
        raise ValueError("Roll number cannot be empty")
    validate_marks(maths, science, english)


def add_student(db, name, roll_number, maths, science, english):
    """Add a new student record to the database."""
    validate_student_data(name, roll_number, maths, science, english)

    percentage = calculate_percentage(maths, science, english)
    grade = calculate_grade(percentage)

    try:
        db.execute(
            """INSERT INTO students (name, roll_number, maths, science, english, percentage, grade)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (name.strip(), roll_number.strip().upper(), maths, science, english, percentage, grade)
        )
        db.commit()
        return {"name": name, "roll_number": roll_number, "percentage": percentage, "grade": grade}
    except sqlite3.IntegrityError:
        raise ValueError(f"Roll number '{roll_number}' already exists")


def get_all_students(db):
    """Retrieve all students from the database."""
    rows = db.execute(
        "SELECT * FROM students ORDER BY percentage DESC"
    ).fetchall()
    return [dict(row) for row in rows]


def get_student_by_id(db, student_id):
    """Retrieve a single student by ID."""
    row = db.execute(
        "SELECT * FROM students WHERE id = ?", (student_id,)
    ).fetchone()
    return dict(row) if row else None


def get_student_by_roll(db, roll_number):
    """Retrieve a student by roll number."""
    row = db.execute(
        "SELECT * FROM students WHERE roll_number = ?", (roll_number.upper(),)
    ).fetchone()
    return dict(row) if row else None


def delete_student(db, student_id):
    """Delete a student record by ID. Returns True if deleted."""
    cursor = db.execute("DELETE FROM students WHERE id = ?", (student_id,))
    db.commit()
    return cursor.rowcount > 0


def get_class_statistics(db):
    """Calculate class-wide statistics."""
    students = get_all_students(db)
    if not students:
        return {"total": 0, "average": 0, "highest": 0, "lowest": 0, "pass_count": 0, "fail_count": 0}

    percentages = [s["percentage"] for s in students]
    pass_count = sum(1 for s in students if s["grade"] != "F")

    return {
        "total": len(students),
        "average": round(sum(percentages) / len(percentages), 2),
        "highest": max(percentages),
        "lowest": min(percentages),
        "pass_count": pass_count,
        "fail_count": len(students) - pass_count,
    }
