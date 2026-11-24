import os
import sys
from dotenv import load_dotenv
from run_sql import run_file

load_dotenv()

if os.getenv("ALLOW_RESET") != "yes":
    sys.exit("Reset blocked: set ALLOW_RESET=yes in .env first.")

run_file("database/reset.sql")
run_file("database/schema.sql")

if os.path.exists("database/seed.sql"):
    run_file("database/seed.sql")
else:
    print("No seed.sql yet, skipped.")