import os
 
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
 
load_dotenv()
 
 
def get_connection():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured")
    return psycopg2.connect(database_url)
 
 
def fetch_all(sql, params=()):
    """Run a SELECT query and return all rows as dictionaries."""
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            return cur.fetchall()
    finally:
        conn.close()
 
 
def fetch_one(sql, params=()):
    """Run a SELECT query and return one row, or None if no row exists."""
    rows = fetch_all(sql, params)
    return rows[0] if rows else None
