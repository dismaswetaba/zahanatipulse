import re
from datetime import date
 
PHONE_PATTERN = re.compile(r"^[0-9+()\- ]{7,30}$")

def validate_patient(data):
    """Check the details sent by the browser.
 
    Returns (clean_values, errors). If errors is not empty, do not save.
    """
    errors = {}
 
    full_name = data.get("full_name")
    if not isinstance(full_name, str) or not full_name.strip():
        errors["full_name"] = "Full name is required."
        full_name = None
    else:
        full_name = " ".join(full_name.split())
        if len(full_name) < 2 or len(full_name) > 150:
            errors["full_name"] = "Full name must be 2 to 150 characters."
 
    date_of_birth = data.get("date_of_birth") or None
    if date_of_birth is not None:
        try:
            date_of_birth = date.fromisoformat(str(date_of_birth))
            if date_of_birth > date.today() or date_of_birth.year < 1900:
                errors["date_of_birth"] = "Date of birth is not valid."
        except ValueError:
            errors["date_of_birth"] = "Use the format YYYY-MM-DD."
 
    phone = data.get("phone")
    if isinstance(phone, str):
        phone = phone.strip() or None
    elif phone is not None:
        errors["phone"] = "Phone must be text."
    if phone and not PHONE_PATTERN.match(phone):
        errors["phone"] = "Phone may contain digits, spaces, + ( ) and - only (7 to 30 characters)."
 
    clean = {
        "full_name": full_name,
        "date_of_birth": date_of_birth,
        "phone": phone,
    }
    return clean, errors
