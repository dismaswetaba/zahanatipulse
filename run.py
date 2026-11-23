import os
from flask import Flask

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def home():
    return "ZahanatiPulse is running"

if __name__ == "__main__":
    app.run(debug=True)