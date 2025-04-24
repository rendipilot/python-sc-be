from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import logging
from  routes.login_routes import login_routes
from routes.predict_routes import predict_routes
from routes.history_routes import history_routes
from routes.teacher_routes import teacher_routes

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

load_dotenv()

CORS(app)

app.register_blueprint(login_routes)
app.register_blueprint(predict_routes)
app.register_blueprint(history_routes)
app.register_blueprint(teacher_routes)

if __name__ == "__main__":
    app.run(debug=True)