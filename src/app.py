from flask import Flask
from dotenv import load_dotenv
from routes import add_routes
from config import Config
from di_container import DIContainer

load_dotenv()

app: Flask = Flask(__name__)
app.container = DIContainer()
app.config.from_object(Config())
add_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["FRONTEND_PORT"])