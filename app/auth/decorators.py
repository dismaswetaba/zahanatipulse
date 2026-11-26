from functools import wraps
from flask import abort, jsonify, redirect, request, session, url_for


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            if request.path.startswith("/api/"):
                return jsonify({"error": "Login required"}), 401
            return redirect(url_for("auth.login_page"))
        return view(*args, **kwargs)
    return wrapped


def role_required(*allowed_roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if session.get("role") not in allowed_roles:
                if request.path.startswith("/api/"):
                    return jsonify({"error": "You do not have permission to do this"}), 403
                abort(403)
            return view(*args, **kwargs)
        return wrapped
    return decorator


def current_user_id():
    return session["user_id"]


def current_facility_id():
    return session["facility_id"]


def role_required(*allowed_roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if session.get("role") not in allowed_roles:
                if request.path.startswith("/api/"):
                    return jsonify({"error": "You do not have permission to do this"}), 403
                abort(403)
            return view(*args, **kwargs)
        return wrapped
    return decorator


def current_user_id():
    return session["user_id"]


def current_facility_id():
    return session["facility_id"]