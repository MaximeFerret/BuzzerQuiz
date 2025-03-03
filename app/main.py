from backend.models.db import db
from backend.models.user import User
from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from backend.controleur.auth_ctrl import auth_bp
#from frontend.blueprints.auth.auth import auth_bp
from frontend.blueprints.buzzer.buzzer import buzzer_bp
from frontend.blueprints.quiz.quiz import quiz_bp

app = Flask(__name__, template_folder="frontend/templates")
app.static_folder = "frontend/static"
app.config.from_object("backend.config.Config")

db.init_app(app)
migrate = Migrate(app, db)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "authentication.login"

csrf = CSRFProtect(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# app.permanent_session_lifetime = app.config['PERMANENT_SESSION_LIFETIME']


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.register_blueprint(auth_bp)
app.register_blueprint(quiz_bp, url_prefix="/quiz")
app.register_blueprint(buzzer_bp, url_prefix="/buzzer")


@app.route("/")
def homepage():
    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crée la base de données si elle n'existe pas encore
    socketio.run(app, host="0.0.0.0", debug=True)
