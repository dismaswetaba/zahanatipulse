import re
 
from flask import Blueprint, jsonify, render_template, request
 
from db import fetch_all, fetch_one, transaction
from app.auth.decorators import (
    login_required,
    role_required,
    current_facility_id,
    current_user_id,
)
from app.patients.validators import validate_patient
 
patients_bp = Blueprint("patients", __name__)
 
NUMBER_PATTERN = re.compile(r"^(.+)-(\d+)$")
 
PATIENT_COLUMNS = """
    patient_id,
    patient_number,
    full_name,
    date_of_birth,
    phone,
    created_at
"""
 
 
def to_json(row):
    """Turn dates and times into text such as 1990-03-14."""
    return {
        key: value.isoformat() if hasattr(value, "isoformat") else value
        for key, value in row.items()
    }
 
 
def next_patient_number(cur, facility_id):
    """Work out the next number for this facility, for example MRU-0007."""
    cur.execute(
        "SELECT patient_number FROM patients WHERE facility_id = %s",
        (facility_id,),
    )
    prefix, highest = "PT", 0
    for row in cur.fetchall():
        match = NUMBER_PATTERN.match(row["patient_number"])
        if match and int(match.group(2)) >= highest:
            prefix, highest = match.group(1), int(match.group(2))
    return f"{prefix}-{highest + 1:04d}"
 
 
# ---------- page ----------
 
@patients_bp.route("/patients")
@login_required
@role_required("receptionist", "clinician")
def patients_page():
    return render_template("patients.html")
 
 
# ---------- API ----------
 
@patients_bp.route("/api/patients", methods=["GET"])
@login_required
@role_required("receptionist", "clinician")
def list_patients():
    search = request.args.get("search", "").strip()
    pattern = f"%{search}%"
 
    patients = fetch_all(
        f"""
        SELECT {PATIENT_COLUMNS}
        FROM patients
        WHERE facility_id = %s
          AND (full_name ILIKE %s OR patient_number ILIKE %s)
        ORDER BY full_name
        LIMIT 50
        """,
        (current_facility_id(), pattern, pattern),
    )
    return jsonify([to_json(p) for p in patients])
 
 
@patients_bp.route("/api/patients", methods=["POST"])
@login_required
@role_required("receptionist")
def create_patient():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):

           return jsonify({"error": "Send the patient details as JSON"}), 400
 
    clean, errors = validate_patient(data)
    if errors:
        return jsonify({"errors": errors}), 400
 
    facility_id = current_facility_id()
 
    with transaction() as cur:
        # Lock this facility's row so two receptionists registering at the
        # same moment cannot be given the same patient number.
        cur.execute(
            "SELECT facility_id FROM facilities WHERE facility_id = %s FOR UPDATE",
            (facility_id,),
        )
        patient_number = next_patient_number(cur, facility_id)
 
        cur.execute(
            f"""
            INSERT INTO patients
                (facility_id, patient_number, full_name,
                 date_of_birth, phone, created_by)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING {PATIENT_COLUMNS}
            """,
            (
                facility_id,
                patient_number,
                clean["full_name"],
                clean["date_of_birth"],
                clean["phone"],
                current_user_id(),
            ),
        )
        patient = cur.fetchone()
 
    return jsonify(to_json(patient)), 201
 
 
@patients_bp.route("/api/patients/<int:patient_id>", methods=["GET"])
@login_required
@role_required("receptionist", "clinician")
def get_patient(patient_id):
    patient = fetch_one(
        f"""
        SELECT {PATIENT_COLUMNS}
        FROM patients
        WHERE patient_id = %s
          AND facility_id = %s
        """,
        (patient_id, current_facility_id()),
    )
 
    if patient is None:
        return jsonify({"error": "Patient not found"}), 404
 
    return jsonify(to_json(patient))
 
 
@patients_bp.route("/api/patients/<int:patient_id>", methods=["PUT"])
@login_required
@role_required("receptionist")
def update_patient(patient_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Send the patient details as JSON"}), 400
        clean, errors = validate_patient(data)
    if errors:
        return jsonify({"errors": errors}), 400
 
    with transaction() as cur:
        cur.execute(
            f"""
            UPDATE patients
            SET full_name = %s,
                date_of_birth = %s,
                phone = %s
            WHERE patient_id = %s
              AND facility_id = %s
            RETURNING {PATIENT_COLUMNS}
            """,
            (
                clean["full_name"],
                clean["date_of_birth"],
                clean["phone"],
                patient_id,
                current_facility_id(),
            ),
        )
        patient = cur.fetchone()
 
    if patient is None:
        return jsonify({"error": "Patient not found"}), 404
 
    return jsonify(to_json(patient))
