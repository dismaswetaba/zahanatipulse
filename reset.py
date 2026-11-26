import os
import sys
from dotenv import load_dotenv
from run_sql import run_file
from seed import run_seed

load_dotenv()

if os.getenv("ALLOW_RESET") != "yes":
    sys.exit("Reset blocked: set ALLOW_RESET=yes in .env first.")

run_file("database/reset.sql")
run_file("database/schema.sql")
run_seed()