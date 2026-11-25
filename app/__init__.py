import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)

    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        raise RuntimeError("SECRET_KEY is missing from .env")

    app.config["SECRET_KEY"] = secret_key
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    # Remains False for local HTTP; set FLASK_ENV=production for HTTPS
    app.config["SESSION_COOKIE_SECURE"] = (
        os.getenv("FLASK_ENV") == "production"
    )

    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app
