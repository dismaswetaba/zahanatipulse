from flask import Blueprint, jsonify

from db import fetch_one
from app.auth.decorators import (
    login_required,
    role_required,
    current_facility_id,
)

patients_bp = Blueprint("patients", __name__)


@patients_bp.route("/api/patients/<int:patient_id>")
@login_required
@role_required("receptionist", "clinician")
def get_patient(patient_id):
    patient = fetch_one(
        """
        SELECT
            patient_id,
            patient_number,
            full_name,
            date_of_birth,
            phone,
            created_at
        FROM patients
        WHERE patient_id = %s
          AND facility_id = %s
        """,
        (patient_id, current_facility_id()),
    )

    if patient is None:
        return jsonify({"error": "Patient not found"}), 404

    return jsonify(patient)