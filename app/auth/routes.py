from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from db import get_connection, fetch_all
from app.auth.decorators import login_required, role_required, current_facility_id

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("auth.dashboard"))
    return redirect(url_for("auth.login_page"))


@auth_bp.route("/login")
def login_page():
    return render_template("login.html")


@auth_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

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
    return jsonify({
        "user_id": session["user_id"],
        "full_name": session["full_name"],
        "role": session["role"],
        "facility_id": session["facility_id"],
        "facility_name": session["facility_name"],
    })

@auth_bp.route("/api/staff")
@login_required
@role_required("admin")
def list_staff():
    staff = fetch_all(
        """
        SELECT user_id, full_name, email, role, is_active
        FROM users
        WHERE facility_id = %s
        ORDER BY role, full_name
        """,
        (current_facility_id(),),
    )
    return jsonify(staff)