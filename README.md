# Student Result Management System

A full-stack web application to manage and display student results, built with Python Flask, SQLite, and a complete DevOps CI/CD pipeline.

---

## Project Overview

This application allows users to:
- Add students with subject marks (Maths, Science, English)
- Automatically calculate percentage and assign grade (A+/A/B/C/D/F)
- View all students ranked by performance on a dashboard
- View individual student result cards
- Delete student records
- Search student by roll number
- View class statistics (average, highest, pass/fail count)

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11 + Flask |
| Database | SQLite (persistent storage) |
| Frontend | HTML5 + CSS3 (Jinja2 templates) |
| Testing | pytest + pytest-cov |
| Code Quality | SonarCloud |
| Containerization | Docker |
| CI/CD | GitHub Actions |
| Deployment | Render |

---

## Project Structure

```
student-result-system/
├── .github/
│   └── workflows/
│       └── main.yml             # CI/CD pipeline
├── app/
│   ├── __init__.py              # App factory
│   ├── database.py              # SQLite setup & connection
│   ├── models.py                # (data definitions)
│   ├── services.py              # Business logic & grade calculation
│   ├── routes.py                # Web + API routes
│   └── templates/
│       ├── base.html            # Base layout with navbar
│       ├── index.html           # Dashboard with stats + table
│       ├── add_student.html     # Add student form (with live preview)
│       ├── student_detail.html  # Individual result card
│       └── search_result.html   # Search by roll number
├── tests/
│   ├── test_grades.py           # Grade & percentage calculation tests
│   ├── test_students.py         # Add/delete/fetch student tests
│   └── test_statistics.py       # Class statistics tests
├── app.py                       # Entry point
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── sonar-project.properties
└── README.md
```

---

## How to Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/student-result-system.git
cd student-result-system
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the application**
```bash
python app.py
```

Visit: **http://localhost:5000**

The SQLite database (`students.db`) is created automatically on first run.

---

## How to Run Tests

```bash
pytest tests/ -v
```

With coverage report:
```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

Expected: **25+ tests passing**

---

## Docker Setup

**Build the image:**
```bash
docker build -t student-result-system .
```

**Run the container:**
```bash
docker run -p 5000:5000 student-result-system
```

Visit: **http://localhost:5000**

---

## CI/CD Pipeline

Pipeline runs automatically on every push to `main` or `dev`:

```
Code push to GitHub
       ↓
Install Python dependencies
       ↓
Run pytest tests (fails here if tests fail)
       ↓
SonarCloud static code analysis
       ↓
Build Docker image
       ↓
Deploy to Render (main branch only)
```

Pipeline file: `.github/workflows/main.yml`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Dashboard (HTML) |
| GET | `/add` | Add student form |
| POST | `/add` | Submit new student |
| GET | `/student/<id>` | View result card |
| POST | `/delete/<id>` | Delete student |
| GET | `/search?roll=CS001` | Search by roll number |
| GET | `/api/students` | All students (JSON) |
| POST | `/api/students` | Add student (JSON) |
| DELETE | `/api/students/<id>` | Delete student (JSON) |
| GET | `/api/stats` | Class statistics (JSON) |

**Example POST to `/api/students`:**
```json
{
  "name": "Rahul Sharma",
  "roll_number": "CS2024001",
  "maths": 85,
  "science": 90,
  "english": 78
}
```

---

## Grading System

| Percentage | Grade |
|-----------|-------|
| 90 – 100 | A+ |
| 80 – 89 | A |
| 70 – 79 | B |
| 60 – 69 | C |
| 50 – 59 | D |
| Below 50 | F |

---

## Deployment

Live URL: **https://student-result-system.onrender.com** *(update after deploying)*

Deployed on [Render](https://render.com) via automatic deployment triggered by GitHub Actions on push to `main`.

---

## GitHub Secrets Required

| Secret | Description |
|--------|-------------|
| `SONAR_TOKEN` | From sonarcloud.io |
| `RENDER_DEPLOY_HOOK` | From Render dashboard |
