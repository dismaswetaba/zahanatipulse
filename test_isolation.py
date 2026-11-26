from app import create_app

app = create_app()
DEMO_PASSWORD = "Demo@1234"
failures = 0


def login(client, email):
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": DEMO_PASSWORD},
    )
    assert response.status_code == 200, f"Login failed for {email}"


def check(label, actual, expected):
    global failures
    ok = actual == expected
    if not ok:
        failures += 1
    print(
        f"{'PASS' if ok else 'FAIL'}  {label}  "
        f"(got {actual}, expected {expected})"
    )


# 1. Anonymous user
client = app.test_client()
check(
    "Anonymous -> patient 1",
    client.get("/api/patients/1").status_code,
    401,
)

# 2. Meru receptionist
client = app.test_client()
login(client, "reception.meru@zahanatipulse.test")
check(
    "Meru receptionist -> Meru patient 1",
    client.get("/api/patients/1").status_code,
    200,
)
check(
    "Meru receptionist -> Kisumu patient 7",
    client.get("/api/patients/7").status_code,
    404,
)
check(
    "Meru receptionist -> staff list",
    client.get("/api/staff").status_code,
    403,
)
check(
    "Client-supplied facility_id does not bypass isolation",
    client.get("/api/patients/7?facility_id=2").status_code,
    404,
)

# 3. Kisumu receptionist
client = app.test_client()
login(client, "reception.kisumu@zahanatipulse.test")
check(
    "Kisumu receptionist -> Kisumu patient 7",
    client.get("/api/patients/7").status_code,
    200,
)
check(
    "Kisumu receptionist -> Meru patient 1",
    client.get("/api/patients/1").status_code,
    404,
)

# 4. Meru pharmacist
client = app.test_client()
login(client, "pharmacy.meru@zahanatipulse.test")
check(
    "Meru pharmacist -> patient 1",
    client.get("/api/patients/1").status_code,
    403,
)

# 5. Meru administrator
client = app.test_client()
login(client, "admin.meru@zahanatipulse.test")
check(
    "Meru admin -> staff list",
    client.get("/api/staff").status_code,
    200,
)
check(
    "Meru admin -> patient records is forbidden",
    client.get("/api/patients/1").status_code,
    403,
)

staff = client.get("/api/staff").get_json()
check("Meru admin sees 4 staff", len(staff), 4)
check(
    "Meru admin sees no Kisumu staff",
    any("kisumu" in item["email"].lower() for item in staff),
    False,
)
check(
    "Staff list hides password hashes",
    any("password_hash" in item for item in staff),
    False,
)

print()
print("ALL TESTS PASSED" if failures == 0 else f"{failures} TEST(S) FAILED")