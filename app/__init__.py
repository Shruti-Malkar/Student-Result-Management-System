from flask import Flask
from .database import init_db
from .routes import student_bp
import os

def create_app():
    app = Flask(__name__)
    app.config["DATABASE"] = "students.db"
    app.config["TESTING"] = False

    app.secret_key = os.urandom(24) 

    init_db(app)

    app.register_blueprint(student_bp)

    return app
