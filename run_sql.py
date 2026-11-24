import sys
from db import get_connection

def run_file(path):
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
