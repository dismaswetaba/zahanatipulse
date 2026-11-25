from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash
from db import get_connection
from app.auth.decorators import login_required

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("auth.dashboard"))
    return redirect(url_for("auth.login_page"))


@auth_bp.route("/login")
def login_page():
    if "user_id" in session:
        return redirect(url_for("auth.dashboard"))
    return render_template("login.html")


@auth_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid request data"}), 400

    email = data.get("email", "")
    password = data.get("password", "")

    if not isinstance(email, str) or not isinstance(password, str):
        return jsonify({"error": "Invalid input"}), 400

    email = email.strip().lower()
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT u.user_id, u.full_name, u.password_hash, u.role,
                       u.facility_id, f.name
                FROM users u
                JOIN facilities f ON f.facility_id = u.facility_id
                WHERE u.email = %s AND u.is_active = TRUE
                """,
                (email,),
            )
            row = cur.fetchone()
    finally:
        conn.close()

    if row is None or not check_password_hash(row[2], password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Clear any old session data before creating the authenticated session
    session.clear()
    session["user_id"] = row[0]
    session["full_name"] = row[1]
    session["role"] = row[3]
    session["facility_id"] = row[4]
    session["facility_name"] = row[5]

    return jsonify({"message": "Logged in", "role": row[3]})


@auth_bp.route("/api/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})


@auth_bp.route("/api/auth/me")
@login_required
def me():
    return jsonify(
        {
            "user_id": session["user_id"],
            "full_name": session["full_name"],
            "role": session["role"],
            "facility_id": session["facility_id"],
            "facility_name": session["facility_name"],
        }
    )
