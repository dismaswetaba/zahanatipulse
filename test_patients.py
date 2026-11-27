from app import create_app
from db import get_connection
 
app = create_app()
DEMO_PASSWORD = "Demo@1234"
failures = 0
created_ids = []
 
 
def login(client, email):
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": DEMO_PASSWORD},
    )
    assert response.status_code == 200, f"Login failed for {email}"
    return client
 
 
def check(label, actual, expected):
    global failures
    ok = actual == expected
    if not ok:
        failures += 1
    print(
        f"{'PASS' if ok else 'FAIL'}  {label}  "
        f"(got {actual}, expected {expected})"
    )
 
 
meru_reception = login(app.test_client(), "reception.meru@zahanatipulse.test")
meru_clinician = login(app.test_client(), "clinician.meru@zahanatipulse.test")
meru_pharmacist = login(app.test_client(), "pharmacy.meru@zahanatipulse.test")
kisumu_reception = login(app.test_client(), "reception.kisumu@zahanatipulse.test")
anonymous = app.test_client()
 
# --- Access control ---
check("Anonymous -> patient list", anonymous.get("/api/patients").status_code, 401)
check("Pharmacist -> patient list", meru_pharmacist.get("/api/patients").status_code, 403)
check(
    "Clinician cannot register a patient",
    meru_clinician.post("/api/patients", json={"full_name": "Test Person"}).status_code,
    403,
)
 
# --- Registering ---
response = meru_reception.post(
    "/api/patients",
    json={
        "full_name": "  Test   Patient ",
        "date_of_birth": "1999-05-20",
        "phone": "0711 000 999",
        "facility_id": 2,
    },
)
check("Meru receptionist registers a patient", response.status_code, 201)
patient = response.get_json()
created_ids.append(patient["patient_id"])
check("Name is tidied", patient["full_name"], "Test Patient")
check("Number uses the Meru prefix", patient["patient_number"].startswith("MRU-"), True)
check("Date of birth is text", patient["date_of_birth"], "1999-05-20")
check(
    "Meru can read the new patient",
    meru_reception.get(f"/api/patients/{patient['patient_id']}").status_code,
    200,
)
check(
    "Kisumu cannot read it (facility_id in the body was ignored)",
    kisumu_reception.get(f"/api/patients/{patient['patient_id']}").status_code,
    404,
)
 
second = meru_reception.post("/api/patients", json={"full_name": "Second Test"}).get_json()
created_ids.append(second["patient_id"])
first_number = int(patient["patient_number"].split("-")[1])
second_number = int(second["patient_number"].split("-")[1])
check("Numbers go up by one", second_number, first_number + 1)
 
# --- Validation ---
check("Empty name is rejected", meru_reception.post("/api/patients", json={"full_name": "  "}).status_code, 400)
check("Future date of birth is rejected", meru_reception.post("/api/patients", json={"full_name": "Future Kid", "date_of_birth": "2999-01-01"}).status_code, 400)
check("Bad date format is rejected", meru_reception.post("/api/patients", json={"full_name": "Bad Date", "date_of_birth": "14/03/1990"}).status_code, 400)
check("Bad phone is rejected", meru_reception.post("/api/patients", json={"full_name": "Bad Phone", "phone": "abc"}).status_code, 400)
check("Non-JSON body is rejected", meru_reception.post("/api/patients", data="hello", content_type="text/plain").status_code, 400)
 
# --- Searching ---
found = meru_reception.get("/api/patients?search=wanjiru").get_json()
check("Meru search finds Mary Wanjiru", [p["full_name"] for p in found], ["Mary Wanjiru"])
check("Kisumu search for the same name finds nobody", kisumu_reception.get("/api/patients?search=wanjiru").get_json(), [])
check("Meru cannot find a Kisumu number", meru_reception.get("/api/patients?search=KSM-0001").get_json(), [])
meru_list = meru_reception.get("/api/patients").get_json()
check("Meru list only has Meru numbers", all(p["patient_number"].startswith("MRU-") for p in meru_list), True)
kisumu_list = kisumu_reception.get("/api/patients").get_json()
check("Kisumu list only has Kisumu numbers", all(p["patient_number"].startswith("KSM-") for p in kisumu_list), True)
check("Clinician can search", meru_clinician.get("/api/patients?search=mary").status_code, 200)
 
# --- Updating ---
pid = patient["patient_id"]
updated = meru_reception.put(f"/api/patients/{pid}", json={"full_name": "Test Patient Updated", "phone": "0722 000 111"})
check("Receptionist updates a patient", updated.status_code, 200)
check("Update is saved", updated.get_json()["phone"], "0722 000 111")
check("Kisumu cannot update a Meru patient", kisumu_reception.put(f"/api/patients/{pid}", json={"full_name": "Hacked"}).status_code, 404)
check("Clinician cannot update", meru_clinician.put(f"/api/patients/{pid}", json={"full_name": "Hacked"}).status_code, 403)
check("Name was not changed by the blocked attempts", meru_reception.get(f"/api/patients/{pid}").get_json()["full_name"], "Test Patient Updated")
 
# --- Pages ---
check("Receptionist opens the patients page", meru_reception.get("/patients").status_code, 200)
check("Receptionist sees the register form", b"Register a new patient" in meru_reception.get("/patients").data, True)
check("Clinician opens the patients page", meru_clinician.get("/patients").status_code, 200)
check("Clinician does not see the register form", b"Register a new patient" in meru_clinician.get("/patients").data, False)
check("Pharmacist is blocked from the page", meru_pharmacist.get("/patients").status_code, 403)
check("Anonymous is sent to login", anonymous.get("/patients").status_code, 302)
 
# --- Clean up the test patients ---
conn = get_connection()
with conn:
    with conn.cursor() as cur:
        for patient_id in created_ids:
            cur.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))
conn.close()
 
print()
print("ALL TESTS PASSED" if failures == 0 else f"{failures} TEST(S) FAILED")
