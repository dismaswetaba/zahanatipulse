import os

from flask import Flask, session
from dotenv import load_dotenv

from app.menu import MENU

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")

    if not app.secret_key:
        raise RuntimeError("SECRET_KEY is not configured")

    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    # Enable this in production when the site is served over HTTPS:
    # app.config["SESSION_COOKIE_SECURE"] = True

    @app.context_processor
    def inject_navigation():
        role = session.get("role")
        return {
            "menu": [
                item for item in MENU
                if role in item["roles"]
            ]
        }

    from app.auth.routes import auth_bp
    from app.patients.routes import patients_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(patients_bp)

    return app
