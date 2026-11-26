import os
import sys
from dotenv import load_dotenv
from db import get_connection

load_dotenv()


def run_file(path):
    name = os.path.basename(path).lower()
    if "reset" in name and os.getenv("ALLOW_RESET") != "yes":
        sys.exit("Blocked: this file deletes data. Set ALLOW_RESET=yes in .env to allow it.")

    with open(path) as f:
        sql = f.read()

    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql)
        print(f"Ran {path} successfully")
    finally:
        conn.close()


if __name__ == "__main__":
    run_file(sys.argv[1])