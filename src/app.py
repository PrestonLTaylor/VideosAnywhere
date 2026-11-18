from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

# TODO: Port should be an int, os.getenv returns a string.
FRONTEND_PORT = os.getenv("FRONTEND_PORT") or 5000

app = Flask(__name__)

@app.route("/")
def home():
    return "Ping!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=FRONTEND_PORT)