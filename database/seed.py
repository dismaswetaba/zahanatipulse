from werkzeug.security import generate_password_hash
from db import get_connection

DEMO_PASSWORD = "Demo@1234"


def run_seed(path="database/seed.sql"):
    with open(path) as f:
        sql = f.read()

    sql = sql.replace("__PASSWORD_HASH__", generate_password_hash(DEMO_PASSWORD))

    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql)
        print("Seed data loaded successfully")
    finally:
        conn.close()


if __name__ == "__main__":
    run_seed()