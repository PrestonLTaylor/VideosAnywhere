from flask import Flask, render_template
from dotenv import load_dotenv
import os

load_dotenv()

frontend_port_env = os.getenv("FRONTEND_PORT") or ""
FRONTEND_PORT = int(frontend_port_env) if frontend_port_env.isdecimal() else 5000

app = Flask(__name__)

@app.route("/")
def home() -> str:
    """
    Displays the index.html inside the template folder for the home page.
    """
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=FRONTEND_PORT)