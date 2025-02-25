from blueprints.auth.auth import auth_bp
from blueprints.quiz.quiz import quiz_bp
from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from models.db import db
from models.user import User

app = Flask(__name__)
app.config.from_object("config.Config")
db.init_app(app)
migrate = Migrate(app, db)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "authentication.login"

csrf = CSRFProtect(app)

# app.permanent_session_lifetime = app.config['PERMANENT_SESSION_LIFETIME']


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.register_blueprint(auth_bp)
app.register_blueprint(quiz_bp, url_prefix="/quiz")


@app.route("/")
def homepage():
    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crée la base de données si elle n'existe pas encore
    app.run(debug=True)
