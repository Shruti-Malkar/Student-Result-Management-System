from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from .database import get_db
from . import services

student_bp = Blueprint("students", __name__)


@student_bp.route("/")
def index():
    """Home page — show all students and class stats."""
    db = get_db()
    students = services.get_all_students(db)
    stats = services.get_class_statistics(db)
    return render_template("index.html", students=students, stats=stats)


@student_bp.route("/add", methods=["GET", "POST"])
def add_student():
    """Add a new student via form."""
    if request.method == "POST":
        name = request.form.get("name")
        roll_number = request.form.get("roll_number")

        try:
            maths = int(request.form.get("maths", 0))
            science = int(request.form.get("science", 0))
            english = int(request.form.get("english", 0))
        except ValueError:
            flash("Marks must be valid numbers.", "error")
            return render_template("add_student.html")

        db = get_db()
        try:
            services.add_student(db, name, roll_number, maths, science, english)
            flash(f"Student '{name}' added successfully!", "success")
            return redirect(url_for("students.index"))
        except ValueError as e:
            flash(str(e), "error")
            return render_template("add_student.html")

    return render_template("add_student.html")


@student_bp.route("/student/<int:student_id>")
def view_student(student_id):
    """View a single student's result card."""
    db = get_db()
    student = services.get_student_by_id(db, student_id)
    if not student:
        flash("Student not found.", "error")
        return redirect(url_for("students.index"))
    return render_template("student_detail.html", student=student)


@student_bp.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    """Delete a student record."""
    db = get_db()
    deleted = services.delete_student(db, student_id)
    if deleted:
        flash("Student record deleted successfully.", "success")
    else:
        flash("Student not found.", "error")
    return redirect(url_for("students.index"))


@student_bp.route("/search")
def search():
    """Search student by roll number."""
    roll = request.args.get("roll", "").strip()
    if not roll:
        return redirect(url_for("students.index"))
    db = get_db()
    student = services.get_student_by_roll(db, roll)
    return render_template("search_result.html", student=student, roll=roll)


# ── REST API endpoints (for CI/CD demo & Postman) ──────────────────────────

@student_bp.route("/api/students", methods=["GET"])
def api_get_students():
    db = get_db()
    return jsonify(services.get_all_students(db)), 200


@student_bp.route("/api/students", methods=["POST"])
def api_add_student():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400
    db = get_db()
    try:
        result = services.add_student(
            db,
            data.get("name"),
            data.get("roll_number"),
            data.get("maths", 0),
            data.get("science", 0),
            data.get("english", 0),
        )
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@student_bp.route("/api/students/<int:student_id>", methods=["DELETE"])
def api_delete_student(student_id):
    db = get_db()
    deleted = services.delete_student(db, student_id)
    if not deleted:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"message": "Deleted successfully"}), 200


@student_bp.route("/api/stats", methods=["GET"])
def api_stats():
    db = get_db()
    return jsonify(services.get_class_statistics(db)), 200
