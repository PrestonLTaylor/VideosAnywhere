from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

FRONTEND_PORT = os.getenv("FRONTEND_PORT") or 5000

app = Flask(__name__)

if __name__ == "__main__":
    app.run(port=FRONTEND_PORT)