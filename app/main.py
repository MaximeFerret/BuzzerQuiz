import os

from backend.business_object.db import db
from backend.business_object.user import User
from backend.controller.quiz_ctrl import quiz_bp
from backend.controller.user_ctrl import auth_bp
from backend.utils.socketio_events import socketio
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate

dotenv_path = "/home/ensai/BuzzerQuiz/app/.env/.env"
load_dotenv(dotenv_path=dotenv_path)

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///buzzerquiz.db")

# Affichage des variables pour vérifier si elles sont bien chargées
print(f"SECRET_KEY: {SECRET_KEY}")
print(f"DATABASE URI: {DATABASE_URI}")


app = Flask(__name__, template_folder="frontend/templates")
app.config.from_object("backend.config.Config")
socketio.init_app(app)

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(auth_bp)
app.register_blueprint(quiz_bp, url_prefix="/quiz")


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "authentication.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def homepage():
    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        # print("Flask URL Map:", app.url_map)

        db.create_all()

    import socket

    # pour avoir l'ip locale si elle ne s'affiche pas ou si elle est 127.0.0.1
    def get_local_ip():
        return socket.gethostbyname(socket.gethostname())

    local_ip = get_local_ip()
    print(f"Accède à l'application sur : http://{local_ip}:5000")

    socketio.run(app, host="0.0.0.0", debug=True)
